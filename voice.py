"""
EON Voice
========
Voice input and output layer for EON.

Supports:
- Text-to-speech with pyttsx3
- Speech recognition with SpeechRecognition
- Wake-word foundation
- Voice authentication foundation

The system safely falls back to text mode when
voice libraries or hardware are unavailable.
"""

import threading


class Voice:
    """EON voice controller."""

    def __init__(self):

        self.enabled = True
        self.status_state = "READY"

        self.tts_engine = None
        self.stt_engine = None

        self.wake_word = "EON"

        self.voice_profile = None
        self.last_text = None

        self._speaking = False

        self._load_tts()
        self._load_stt()

    # =========================================================
    # TEXT TO SPEECH
    # =========================================================

    def _load_tts(self):

        try:

            import pyttsx3

            self.tts_engine = (
                pyttsx3.init()
            )

            self.status_state = "READY"

        except Exception:

            self.tts_engine = None

    # =========================================================
    # SPEECH TO TEXT
    # =========================================================

    def _load_stt(self):

        try:

            import speech_recognition as sr

            self.stt_engine = sr

        except Exception:

            self.stt_engine = None

    # =========================================================
    # LISTEN
    # =========================================================

    def listen(self):

        if self.stt_engine is None:

            return None

        try:

            recognizer = (
                self.stt_engine.Recognizer()
            )

            with self.stt_engine.Microphone() as source:

                self.status_state = "LISTENING"

                recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5
                )

                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=15
                )

            self.status_state = "READY"

            text = recognizer.recognize_google(
                audio
            )

            self.last_text = text

            return text

        except Exception:

            self.status_state = "READY"

            return None

    # =========================================================
    # PROCESS VOICE COMMAND
    # =========================================================

    def process_command(
        self,
        text
    ):

        if not text:

            return None

        text = text.strip()

        if not text:

            return None

        self.last_text = text

        return text

    # =========================================================
    # SPEAK
    # =========================================================

    def speak(
        self,
        text
    ):

        if not text:

            return False

        # -----------------------------------------------------
        # If TTS is unavailable, safely fall back.
        # -----------------------------------------------------

        if self.tts_engine is None:

            return False

        try:

            self._speaking = True
            self.status_state = "SPEAKING"

            self.tts_engine.say(
                str(text)
            )

            self.tts_engine.runAndWait()

            self._speaking = False
            self.status_state = "READY"

            return True

        except Exception:

            self._speaking = False
            self.status_state = "READY"

            return False

    # =========================================================
    # STOP SPEAKING
    # =========================================================

    def stop_speaking(self):

        try:

            if self.tts_engine is not None:

                self.tts_engine.stop()

        except Exception:

            pass

        self._speaking = False
        self.status_state = "READY"

        return True

    # =========================================================
    # WAKE WORD
    # =========================================================

    def detect_wake_word(
        self,
        text
    ):

        if not text:

            return False

        words = text.lower().split()

        return self.wake_word.lower() in words

    # =========================================================
    # WAKE WORD SETUP
    # =========================================================

    def set_wake_word(
        self,
        wake_word
    ):

        if not wake_word:

            return False

        self.wake_word = (
            wake_word.strip()
        )

        return True

    # =========================================================
    # VOICE PROFILE
    # =========================================================

    def set_voice_profile(
        self,
        profile
    ):

        if profile is None:

            return False

        self.voice_profile = profile

        return True

    # =========================================================
    # VOICE VERIFICATION
    # =========================================================

    def verify_voice(
        self,
        audio_data=None
    ):

        """
        Foundation for future voice authentication.

        This currently does not claim to authenticate
        a person's identity.
        """

        if self.voice_profile is None:

            return False

        # Real biometric verification can be
        # connected here later.

        return False

    # =========================================================
    # CONNECT ENGINES
    # =========================================================

    def connect_engines(self):

        self._load_tts()
        self._load_stt()

        return {

            "tts":
                self.tts_engine is not None,

            "stt":
                self.stt_engine is not None,
        }

    # =========================================================
    # STATUS
    # =========================================================

    def status(self):

        return {

            "enabled":
                self.enabled,

            "status":
                self.status_state,

            "tts":
                "CONNECTED"
                if self.tts_engine is not None
                else "UNAVAILABLE",

            "stt":
                "CONNECTED"
                if self.stt_engine is not None
                else "UNAVAILABLE",

            "wake_word":
                self.wake_word,

            "voice_profile":
                "CONFIGURED"
                if self.voice_profile is not None
                else "NOT_CONFIGURED",

            "last_text":
                self.last_text,

        }

    # =========================================================
    # RESET
    # =========================================================

    def reset(self):

        self.stop_speaking()

        self.last_text = None

        self.status_state = "READY"

        return True
