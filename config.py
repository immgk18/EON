"""
EON Configuration
=================
Central configuration for the EON system.
"""

import os


class Config:
    """Global EON configuration."""

    # ─────────────────────────────────────
    # EON IDENTITY
    # ─────────────────────────────────────

    NAME = "EON"
    FULL_NAME = "Executive Orchestration Network"
    VERSION = "4.0"
    MODE = os.getenv("EON_MODE", "NORMAL")

    # ─────────────────────────────────────
    # AI ENGINE
    # ─────────────────────────────────────

    AI_PROVIDER = os.getenv("AI_PROVIDER", "local")
    AI_MODEL = os.getenv("AI_MODEL", "")

    # ─────────────────────────────────────
    # VOICE
    # ─────────────────────────────────────

    VOICE_ENABLED = True
    VOICE_LANGUAGE = os.getenv("VOICE_LANGUAGE", "en-IN")
    WAKE_WORD = os.getenv("WAKE_WORD", "EON")

    # Voice identity
    VOICE_AUTH_ENABLED = True

    # ─────────────────────────────────────
    # MEMORY
    # ─────────────────────────────────────

    MEMORY_ENABLED = True
    MEMORY_DATABASE = os.getenv(
        "MEMORY_DATABASE",
        "eon.db"
    )

    # ─────────────────────────────────────
    # VISION
    # ─────────────────────────────────────

    VISION_ENABLED = True

    # ─────────────────────────────────────
    # WEB INTELLIGENCE
    # ─────────────────────────────────────

    WEB_ENABLED = True

    # ─────────────────────────────────────
    # COMPUTER CONTROL
    # ─────────────────────────────────────

    COMPUTER_CONTROL_ENABLED = True

    # Sensitive computer actions should require
    # additional confirmation.
    REQUIRE_CONFIRMATION = True

    # ─────────────────────────────────────
    # TASK / AGENT SYSTEM
    # ─────────────────────────────────────

    TASK_ENGINE_ENABLED = True
    AGENTS_ENABLED = True

    # ─────────────────────────────────────
    # SECURITY
    # ─────────────────────────────────────

    SECURITY_ENABLED = True

    # Never allow high-risk operations to bypass
    # the security layer.
    SECURITY_CONFIRMATION_REQUIRED = True

    # ─────────────────────────────────────
    # UI
    # ─────────────────────────────────────

    UI_ENABLED = True

    # Minimal EON interface
    UI_THEME = "DARK"
    ORB_COLOR = "GOLD"
    UI_SHOW_SYSTEM_GRAPHS = False

    # ─────────────────────────────────────
    # SERVER
    # ─────────────────────────────────────

    HOST = os.getenv(
        "EON_HOST",
        "127.0.0.1"
    )

    PORT = int(
        os.getenv(
            "EON_PORT",
            "5000"
        )
    )

    DEBUG = os.getenv(
        "DEBUG",
        "false"
    ).lower() == "true"

    # ─────────────────────────────────────
    # FUTURE HARDWARE
    # ─────────────────────────────────────

    # ESP/hardware is intentionally disabled
    # for the current software build.
    HARDWARE_ENABLED = False


def get_config():
    """Return the EON configuration class."""

    return Config
