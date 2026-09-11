"""
EON
===
Executive Orchestration Network
Main Entry Point
"""

import threading

from core.eon import EON
from api import EONAPI


def start_api(eon):
    """Start the EON API server."""

    api = EONAPI(eon)

    print(
        "\nEON API:"
    )

    print(
        f"http://{eon.status()['name'].lower()}"
        f"-api"
    )

    api.run()


def main():

    # ---------------------------------------------------------
    # Create EON
    # ---------------------------------------------------------

    eon = EON()

    # ---------------------------------------------------------
    # Start API in background
    # ---------------------------------------------------------

    api = EONAPI(eon)

    api_thread = threading.Thread(
        target=api.run,
        kwargs={
            "host": "127.0.0.1",
            "port": 5000,
            "debug": False,
        },
        daemon=True,
    )

    api_thread.start()

    print(
        "EON API started on "
        "http://127.0.0.1:5000"
    )

    # ---------------------------------------------------------
    # Start EON Core
    # ---------------------------------------------------------

    eon.start()


if __name__ == "__main__":

    main()
