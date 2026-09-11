"""
EON Voice
=========
Real voice interaction layer for EON.

Capabilities:
- Speech-to-text interface
- Text-to-speech interface
- Wake-word detection
- Voice command processing
- Voice profile foundation
- Engine connection management

The implementation uses optional local engines.
If an engine is unavailable, EON safely falls back
to text mode.
"""

from datetime import datetime


class VoiceManager:
    """Manages EON's voice interaction system."""

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(
        self,
        wake_word="EON",
        language="en-IN"
    ):

        self.enabled = True

        self.wake_word = wake_word

        self.language = language

        self.is_listening = False
        self.is_speaking = False

        self.last_command = None
        self.last_response = None

        # -----------------------------------------------------
        # Voice authentication
        # -----------------------------------------------------

        self.voice_auth_enabled = True
        self.voice_profile_registered = False
        self.last_verification = None

        # -----------------------------------------------------
        # Engines
        # -----------------------------------------------------

        self.speech_engine = "NOT_CONNECTED"
        self.tts_engine = "NOT_CONNECTED"
        self.verification_engine = "NOT_CONNECTED"

        self.stt = None
        self.tts = None

        # -----------------------------------------------------
        # Try loading optional engines
        # -----------------------------------------------------

        self._load_tts_engine()
        self._load_stt_engine()

    # =========================================================
    # LOAD TTS
    # =========================================================

    def _load_tts_engine(self):

        try:

            import pyttsx3

            self.tts = pyttsx3.init()

            self.tts_engine = "pyttsx3"

        except Exception:

            self.tts = None
            self.tts_engine = "NOT_CONNECTED"

    # =========================================================
    # LOAD STT
    # =========================================================

    def _load_stt_engine(self):

        try:

            import speech_recognition as sr

            self.stt = sr.Recognizer()

            self.speech_engine = (
                "speech_recognition"
            )

        except Exception:

            self.stt = None
            self.speech_engine = "NOT_CONNECTED"

    # =========================================================
    # ENABLE
    # =========================================================

    def enable(self):

        self.enabled = True

        return True

    # =========================================================
    # DISABLE
    # =========================================================

    def disable(self):

        self.enabled = False

        self.is_listening = False
        self.is_speaking = False

        return True

    # =========================================================
    # START LISTENING
    # =========================================================

    def start_listening(self):

        if not self.enabled:

            return {
                "success": False,
                "status": "DISABLED",
                "message":
                    "Voice system is disabled.",
            }

        self.is_listening = True

        return {
            "success": True,
            "status": "LISTENING",
            "message":
                "EON is listening.",
        }

    # =========================================================
    # STOP LISTENING
    # =========================================================

    def stop_listening(self):

        self.is_listening = False

        return {
            "success": True,
            "status": "STOPPED",
            "message":
                "EON stopped listening.",
        }

    # =========================================================
    # LISTEN FROM MICROPHONE
    # =========================================================

    def listen(self):

        if not self.enabled:

            return None

        if self.stt is None:

            return None

        try:

            import speech_recognition as sr

            with sr.Microphone() as source:

                self.is_listening = True

                print(
                    "EON: Listening..."
                )

                self.stt.adjust_for_ambient_noise(
                    source,
                    duration=0.5
                )

                audio = self.stt.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=10
                )

            self.is_listening = False

            # -------------------------------------------------
            # Speech recognition
            # -------------------------------------------------

            try:

                text = self.stt.recognize_google(
                    audio,
                    language=self.language
                )

            except (
                sr.UnknownValueError,
                sr.RequestError
            ):

                return None

            if not text:

                return None

            self.last_command = text

            return text.strip()

        except (
            OSError,
            AttributeError,
            ImportError,
            Exception
        ):

            self.is_listening = False

            return None

    # =========================================================
    # RECEIVE RECOGNIZED TEXT
    # =========================================================

    def receive_text(
        self,
        text
    ):

        if not text:

            return {
                "success": False,
                "message":
                    "No speech was detected.",
            }

        text = text.strip()

        self.last_command = text

        return {
            "success": True,
            "text": text,
            "wake_word_detected":
                self.detect_wake_word(text),
        }

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

        return (
            self.wake_word.lower()
            in words
        )

    # =========================================================
    # REMOVE WAKE WORD
    # =========================================================

    def remove_wake_word(
        self,
        text
    ):

        if not text:

            return ""

        words = text.split()

        wake = (
            self.wake_word.lower()
        )

        filtered = [
            word
            for word in words
            if word.lower() != wake
        ]

        return " ".join(
            filtered
        ).strip()

    # =========================================================
    # PROCESS VOICE COMMAND
    # =========================================================

    def process_command(
        self,
        text,
        voice_data=None
    ):

        if not text:

            return {
                "success": False,
                "message":
                    "No command received.",
            }

        # -----------------------------------------------------
        # Wake word
        # -----------------------------------------------------

        if not self.detect_wake_word(
            text
        ):

            return {
                "success": False,
                "message":
                    "Wake word not detected.",
            }

        # -----------------------------------------------------
        # Voice verification
        # -----------------------------------------------------

        if self.voice_auth_enabled:

            verified = self.verify_voice(
                voice_data
            )

            if not verified:

                return {
                    "success": False,
                    "message":
                        "Voice identity could not "
                        "be verified.",
                }

        # -----------------------------------------------------
        # Extract command
        # -----------------------------------------------------

        command = self.remove_wake_word(
            text
        )

        if not command:

            return {
                "success": True,
                "message":
                    "Wake word detected. "
                    "Waiting for your command.",
                "command": "",
            }

        self.last_command = command

        return {
            "success": True,
            "command": command,
            "message":
                "Voice command accepted.",
        }

    # =========================================================
    # TEXT TO SPEECH
    # =========================================================

    def speak(
        self,
        text
    ):

        if not text:

            return False

        if not self.enabled:

            return False

        self.last_response = text

        # -----------------------------------------------------
        # Fallback if TTS unavailable
        # -----------------------------------------------------

        if self.tts is None:

            print(
                f"EON: {text}"
            )

            return True

        try:

            self.is_speaking = True

            self.tts.say(
                text
            )

            self.tts.runAndWait()

            self.is_speaking = False

            return True

        except Exception:

            self.is_speaking = False

            print(
                f"EON: {text}"
            )

            return False

    # =========================================================
    # STOP SPEAKING
    # =========================================================

    def stop_speaking(self):

        if self.tts is not None:

            try:

                self.tts.stop()

            except Exception:

                pass

        self.is_speaking = False

        return True

    # =========================================================
    # VOICE PROFILE
    # =========================================================

    def register_voice_profile(
        self,
        voice_data=None
    ):

        if voice_data is None:

            return {
                "success": False,
                "status":
                    "VERIFICATION_ENGINE_REQUIRED",
                "message":
                    "A speaker verification engine "
                    "must be connected first.",
            }

        self.voice_profile_registered = True

        return {
            "success": True,
            "status": "REGISTERED",
            "message":
                "Voice profile registered.",
        }

    # =========================================================
    # VERIFY VOICE
    # =========================================================

    def verify_voice(
        self,
        voice_data=None
    ):

        if not self.voice_auth_enabled:

            self.last_verification = {
                "verified": True,
                "reason":
                    "Voice authentication disabled.",
            }

            return True

        if not self.voice_profile_registered:

            self.last_verification = {
                "verified": False,
                "reason":
                    "No voice profile registered.",
            }

            return False

        if voice_data is None:

            self.last_verification = {
                "verified": False,
                "reason":
                    "No voice data supplied.",
            }

            return False

        # -----------------------------------------------------
        # Real speaker verification will be connected later.
        # -----------------------------------------------------

        self.last_verification = {
            "verified": False,
            "reason":
                "Speaker verification engine "
                "is not connected.",
        }

        return False

    # =========================================================
    # CONNECT STT
    # =========================================================

    def connect_speech_engine(
        self,
        engine_name
    ):

        if not engine_name:

            return False

        self.speech_engine = (
            engine_name
        )

        return True

    # =========================================================
    # CONNECT TTS
    # =========================================================

    def connect_tts_engine(
        self,
        engine_name
    ):

        if not engine_name:

            return False

        self.tts_engine = (
            engine_name
        )

        return True

    # =========================================================
    # CONNECT VERIFICATION ENGINE
    # =========================================================

    def connect_verification_engine(
        self,
        engine_name
    ):

        if not engine_name:

            return False

        self.verification_engine = (
            engine_name
        )

        return True

    # =========================================================
    # VOICE PROFILE
    # =========================================================

    def get_voice_profile(
        self,
        mode="NORMAL"
    ):

        mode = mode.upper()

        if mode == "KILL":

            return {
                "mode": "KILL",
                "tone": "deep",
                "style": "controlled",
                "intensity": "high",
            }

        return {
            "mode": "NORMAL",
            "tone": "warm",
            "style": "calm",
            "intensity": "normal",
        }

    # =========================================================
    # LAST VERIFICATION
    # =========================================================

    def get_last_verification(self):

        return self.last_verification

    # =========================================================
    # STATUS
    # =========================================================

    def status(self):

        return {

            "enabled":
                self.enabled,

            "language":
                self.language,

            "wake_word":
                self.wake_word,

            "voice_auth":
                self.voice_auth_enabled,

            "profile_registered":
                self.voice_profile_registered,

            "listening":
                self.is_listening,

            "speaking":
                self.is_speaking,

            "speech_engine":
                self.speech_engine,

            "tts_engine":
                self.tts_engine,

            "verification_engine":
                self.verification_engine,

            "timestamp":
                datetime.now().isoformat(),
        }
