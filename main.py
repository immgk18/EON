"""
EON - Executive Orchestration Network
Main Entry Point

This file starts the EON Core.
"""

from core.eon import EON


def main():
    """Start EON."""

    print()
    print("Starting EON...")
    print()

    try:
        eon = EON()
        eon.start()

    except KeyboardInterrupt:
        print()
        print("EON: Shutdown requested.")
        print("EON: Goodbye.")

    except Exception as error:
        print()
        print("EON: A system error occurred.")
        print(f"EON: {error}")


if __name__ == "__main__":
    main()
