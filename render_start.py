"""
EON Render Startup
==================
Cloud deployment entry point.
"""

from core.eon import EON
from api import EONAPI


# Create EON Core
eon = EON()

# Create API
api = EONAPI(eon)

# Render exposes the PORT environment variable.
# Flask will use the port assigned by Render.

application = api.app


if __name__ == "__main__":

    import os

    port = int(
        os.getenv(
            "PORT",
            "5000"
        )
    )

    application.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
