"""
EON - Executive Orchestration Network
Main Entry Point
"""

from core.eon import EON


def main():
    """Create and start the EON system."""

    eon = EON()
    eon.start()


if __name__ == "__main__":
    main()
