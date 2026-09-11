"""
EON Render Startup
==================
Entry point used by Render.
"""

from api import EONAPI


def main():
    server = EONAPI()
    server.run()


if __name__ == "__main__":
    main()
