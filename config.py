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

    MODE = os.getenv(
        "EON_MODE",
        "NORMAL"
    ).upper()

    # ─────────────────────────────────────
    # AI ENGINE
    # ─────────────────────────────────────

    # Provider can be changed without modifying
    # the rest of EON.
    AI_PROVIDER = os.getenv(
        "AI_PROVIDER",
        "local"
    )

    # Actual model name will be configured later.
    AI_MODEL = os.getenv(
        "AI_MODEL",
        ""
    )

    AI_TEMPERATURE = float(
        os.getenv(
            "AI_TEMPERATURE",
            "0.7"
        )
    )

    AI_MAX_TOKENS = int(
        os.getenv(
            "AI_MAX_TOKENS",
            "2048"
        )
    )

    # ─────────────────────────────────────
    # VOICE
    # ─────────────────────────────────────

    VOICE_ENABLED = True

    VOICE_LANGUAGE = os.getenv(
        "VOICE_LANGUAGE",
        "en-IN"
    )

    WAKE_WORD = os.getenv(
        "WAKE_WORD",
        "EON"
    )

    # Voice identity is a future biometric
    # integration. Sensitive actions still
    # require security confirmation.
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
    # TASK ENGINE
    # ─────────────────────────────────────

    TASK_ENGINE_ENABLED = True

    # ─────────────────────────────────────
    # AGENT SYSTEM
    # ─────────────────────────────────────

    AGENTS_ENABLED = True

    # ─────────────────────────────────────
    # TOOL SYSTEM
    # ─────────────────────────────────────

    TOOLS_ENABLED = True

    # ─────────────────────────────────────
    # WEB INTELLIGENCE
    # ─────────────────────────────────────

    WEB_ENABLED = True

    # ─────────────────────────────────────
    # VISION
    # ─────────────────────────────────────

    VISION_ENABLED = True

    # ─────────────────────────────────────
    # FILE SYSTEM
    # ─────────────────────────────────────

    FILES_ENABLED = True

    # ─────────────────────────────────────
    # COMPUTER CONTROL
    # ─────────────────────────────────────

    COMPUTER_CONTROL_ENABLED = True

    # Protected actions must require
    # authorization.
    REQUIRE_CONFIRMATION = True

    # ─────────────────────────────────────
    # SECURITY
    # ─────────────────────────────────────

    SECURITY_ENABLED = True

    SECURITY_CONFIRMATION_REQUIRED = True

    # ─────────────────────────────────────
    # USER INTERFACE
    # ─────────────────────────────────────

    UI_ENABLED = True

    UI_THEME = "DARK"

    # Minimal EON visual identity.
    ORB_COLOR = "GOLD"

    # Keep the main interface clean.
    UI_SHOW_SYSTEM_GRAPHS = False

    # ─────────────────────────────────────
    # SERVER / PHONE API
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

    DEBUG = (
        os.getenv(
            "DEBUG",
            "false"
        ).lower()
        == "true"
    )

    # ─────────────────────────────────────
    # FUTURE HARDWARE
    # ─────────────────────────────────────

    # ESP32 / hardware intentionally excluded
    # from the current EON software build.
    HARDWARE_ENABLED = False


def get_config():
    """Return the EON configuration."""

    return Config
