"""
EON API
=======
EON web interface and API server.
"""

import os
import secrets
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from core.eon import EON


class EONAPI:
    """Web API wrapper for EON."""

    def __init__(self):
        self.app = Flask(__name__)

        self.base_dir = Path(__file__).resolve().parent
        self.eon = EON()

        self._register_routes()

    # =====================================================
    # AUTHENTICATION
    # =====================================================

    def authenticate(self):
        expected_token = os.getenv(
            "EON_API_TOKEN",
            ""
        )

        supplied_token = request.headers.get(
            "X-EON-Token",
            ""
        )

        if not expected_token:
            return False

        return secrets.compare_digest(
            supplied_token,
            expected_token
        )

    # =====================================================
    # ROUTES
    # =====================================================

    def _register_routes(self):

        @self.app.route("/", methods=["GET"])
        def home():

            return send_from_directory(
                self.base_dir,
                "index.html"
            )

        # -------------------------------------------------
        # API INFO
        # -------------------------------------------------

        @self.app.route("/api", methods=["GET"])
        def api_info():

            return jsonify({
                "success": True,
                "name": "EON API",
                "system": "EON",
                "version": "1.0",
                "status": "ONLINE",
                "authentication": "TOKEN_REQUIRED"
            })

        # -------------------------------------------------
        # HEALTH
        # -------------------------------------------------

        @self.app.route(
            "/api/health",
            methods=["GET"]
        )
        def health():

            return jsonify({
                "success": True,
                "service": "EON",
                "status": "ONLINE"
            })

        # -------------------------------------------------
        # STATUS
        # -------------------------------------------------

        @self.app.route(
            "/api/status",
            methods=["GET"]
        )
        def status():

            if not self.authenticate():

                return jsonify({
                    "success": False,
                    "error": "Authentication required."
                }), 401

            try:

                return jsonify({
                    "success": True,
                    "status": "ONLINE",
                    "eon": self.eon.status()
                })

            except Exception as error:

                return jsonify({
                    "success": False,
                    "error": str(error)
                }), 500

        # -------------------------------------------------
        # COMMAND
        # -------------------------------------------------

        @self.app.route(
            "/api/command",
            methods=["POST"]
        )
        def command():

            if not self.authenticate():

                return jsonify({
                    "success": False,
                    "error": "Authentication required."
                }), 401

            data = request.get_json(
                silent=True
            )

            if not isinstance(data, dict):

                return jsonify({
                    "success": False,
                    "error": "JSON request body required."
                }), 400

            user_command = data.get(
                "command",
                ""
            )

            if not isinstance(
                user_command,
                str
            ):

                return jsonify({
                    "success": False,
                    "error": "Command must be text."
                }), 400

            user_command = user_command.strip()

            if not user_command:

                return jsonify({
                    "success": False,
                    "error": "Command cannot be empty."
                }), 400

            if len(user_command) > 2000:

                return jsonify({
                    "success": False,
                    "error": "Command is too long."
                }), 400

            try:

                result = self.eon.handle_command(
                    user_command
                )

                return jsonify({
                    "success": True,
                    "command": user_command,
                    "response": result
                })

            except Exception as error:

                return jsonify({
                    "success": False,
                    "error": str(error)
                }), 500

        # -------------------------------------------------
        # MODULES
        # -------------------------------------------------

        @self.app.route(
            "/api/modules",
            methods=["GET"]
        )
        def modules():

            if not self.authenticate():

                return jsonify({
                    "success": False,
                    "error": "Authentication required."
                }), 401

            try:

                return jsonify({
                    "success": True,
                    "modules":
                        self.eon.router.get_available_modules()
                })

            except Exception as error:

                return jsonify({
                    "success": False,
                    "error": str(error)
                }), 500

    # =====================================================
    # RUN SERVER
    # =====================================================

    def run(self):

        port = int(
            os.getenv(
                "PORT",
                "10000"
            )
        )

        self.app.run(
            host="0.0.0.0",
            port=port
        )


# =========================================================
# APPLICATION INSTANCE
# =========================================================

eon_api = EONAPI()

app = eon_api.app


# =========================================================
# DIRECT START
# =========================================================

if __name__ == "__main__":
    eon_api.run()
