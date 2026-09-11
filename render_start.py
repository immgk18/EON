"""
EON Render Start
================
Production entry point for Render.
"""

from api import EONAPI


def main():

    server = EONAPI()

    server.run()


if __name__ == "__main__":
    main()
