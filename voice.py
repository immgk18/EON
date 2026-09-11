"""
EON Voice
=========
Voice interaction layer for EON.

Pipeline:

Microphone
    ↓
Speech Recognition
    ↓
Wake Word
    ↓
Voice Verification
    ↓
Command
    ↓
EON Brain
    ↓
Text-to-Speech

Actual speech recognition, speaker verification,
and TTS engines can be connected through this
interface later.
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

        # -----------------------------------------------------
        # Voice state
        # -----------------------------------------------------

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
        # Engine states
        # -----------------------------------------------------

        self.speech_engine = (
            "NOT_CONNECTED"
        )

        self.tts_engine = (
            "NOT_CONNECTED"
        )

        self.verification_engine = (
            "NOT_CONNECTED"
        )

    # =========================================================
    # ENABLE / DISABLE
    # =========================================================

    def enable(self):

        self.enabled = True

        return True

    def disable(self):

        self.enabled = False

        self.is_listening = False
        self.is_speaking = False

        return True

    # =========================================================
    # LISTENING
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
    # LISTEN
    # =========================================================

    def listen(self):

        if not self.enabled:

            return None

        self.is_listening = True

        # -----------------------------------------------------
        # Actual microphone engine will be connected later.
        # -----------------------------------------------------

        return None

    # =========================================================
    # RECEIVE SPEECH TEXT
    # =========================================================

    def receive_text(
        self,
        text
    ):
        """
        Process text produced by a speech-recognition engine.
        """

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
        """Detect EON's wake word."""

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
        """Remove the wake word from a command."""

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
    # VOICE PROFILE
    # =========================================================

    def register_voice_profile(
        self,
        voice_data=None
    ):
        """
        Register a voice profile.

        The actual speaker-embedding engine will be
        connected later.
        """

        if voice_data is None:

            return {
                "success": False,
                "status":
                    "VOICE_ENGINE_REQUIRED",
                "message":
                    "A voice verification engine "
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
        """
        Verify whether the speaker matches the
        registered voice profile.

        This returns False until a real speaker
        verification engine is connected.
        """

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
        # Real speaker verification goes here.
        # -----------------------------------------------------

        self.last_verification = {
            "verified": False,
            "reason":
                "Voice verification engine "
                "is not connected.",
        }

        return False

    # =========================================================
    # PROCESS VOICE COMMAND
    # =========================================================

    def process_command(
        self,
        text,
        voice_data=None
    ):
        """
        Process a recognized voice command.

        Steps:
        1. Detect wake word
        2. Remove wake word
        3. Verify speaker
        4. Return command
        """

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
        # Voice identity
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
    # SPEAK
    # =========================================================

    def speak(
        self,
        text
    ):
        """
        Send text to the configured TTS engine.

        Until an actual TTS engine is connected,
        EON prints the response.
        """

        if not text:

            return False

        if not self.enabled:

            return False

        self.is_speaking = True

        self.last_response = text

        # -----------------------------------------------------
        # Placeholder output
        # -----------------------------------------------------

        print(
            f"EON: {text}"
        )

        self.is_speaking = False

        return True

    # =========================================================
    # STOP SPEAKING
    # =========================================================

    def stop_speaking(self):

        self.is_speaking = False

        return True

    # =========================================================
    # CONNECT SPEECH ENGINE
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
    # CONNECT TTS ENGINE
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
