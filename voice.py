"""
EON Voice
========
Voice interaction foundation for EON.

Speech recognition, voice identification, and text-to-speech
engines can be connected through this interface later.
"""

from datetime import datetime


class VoiceManager:
    """Manages EON's voice interface."""

    def __init__(self):
        self.enabled = True
        self.voice_auth_enabled = True
        self.wake_word = "EON"
        self.language = "en-IN"

        self.is_listening = False
        self.is_speaking = False

    # ─────────────────────────────────────
    # LISTENING
    # ─────────────────────────────────────

    def start_listening(self):
        """Start listening for voice input."""

        self.is_listening = True

        return {
            "status": "LISTENING",
            "message": "EON is listening."
        }

    def stop_listening(self):
        """Stop listening."""

        self.is_listening = False

        return {
            "status": "STOPPED",
            "message": "EON stopped listening."
        }

    def listen(self):
        """
        Capture voice input.

        Actual speech recognition will be connected later.
        """

        self.is_listening = True

        return None

    # ─────────────────────────────────────
    # WAKE WORD
    # ─────────────────────────────────────

    def detect_wake_word(self, text):
        """Check whether the wake word is present."""

        if not text:
            return False

        return self.wake_word.lower() in text.lower()

    # ─────────────────────────────────────
    # VOICE IDENTITY
    # ─────────────────────────────────────

    def verify_voice(self, voice_data=None):
        """
        Verify the authorized user's voice.

        The actual voice-biometric model will be connected later.
        """

        if not self.voice_auth_enabled:
            return True

        if voice_data is None:
            return False

        # Placeholder until a real voice identity model
        # is connected.
        return False

    # ─────────────────────────────────────
    # SPEAKING
    # ─────────────────────────────────────

    def speak(self, text):
        """
        Convert text into speech.

        Actual text-to-speech engine will be connected later.
        """

        if not text:
            return False

        self.is_speaking = True

        print(f"EON: {text}")

        self.is_speaking = False

        return True

    # ─────────────────────────────────────
    # MODE VOICES
    # ─────────────────────────────────────

    def get_voice_profile(self, mode="NORMAL"):
        """Return the voice profile for the current EON mode."""

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

    # ─────────────────────────────────────
    # STATUS
    # ─────────────────────────────────────

    def status(self):
        """Return current voice system status."""

        return {
            "enabled": self.enabled,
            "language": self.language,
            "wake_word": self.wake_word,
            "voice_auth": self.voice_auth_enabled,
            "listening": self.is_listening,
            "speaking": self.is_speaking,
            "timestamp": datetime.now().isoformat(),
        }
