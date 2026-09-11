"""
EON API
=======
Web API + EON browser interface.
"""

import os
import secrets
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from core.eon import EON


# =========================================================
# APP SETUP
# =========================================================

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent

# Create ONE EON instance for the running server
eon = EON()


# =========================================================
# AUTHENTICATION
# =========================================================

def authenticate():
    """
    Check the EON API token.

    The real token must be stored in Render Environment
    Variables as EON_API_TOKEN.
    """

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


# =========================================================
# EON WEB INTERFACE
# =========================================================

@app.route("/", methods=["GET"])
def home():
    """
    Serve the EON interface.
    """

    return send_from_directory(
        BASE_DIR,
        "index.html"
    )


# =========================================================
# API INFORMATION
# =========================================================

@app.route("/api", methods=["GET"])
def api_info():

    return jsonify({
        "success": True,
        "name": "EON API",
        "system": "Executive Orchestration Network",
        "version": "1.0",
        "status": "ONLINE",
        "authentication": "TOKEN_REQUIRED"
    })


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/api/health", methods=["GET"])
def health():

    return jsonify({
        "success": True,
        "service": "EON",
        "status": "ONLINE"
    })


# =========================================================
# STATUS
# =========================================================

@app.route("/api/status", methods=["GET"])
def status():

    if not authenticate():

        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    try:

        return jsonify({
            "success": True,
            "status": "ONLINE",
            "eon": eon.status()
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# =========================================================
# COMMAND
# =========================================================

@app.route("/api/command", methods=["POST"])
def command():

    if not authenticate():

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

        result = eon.handle_command(
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


# =========================================================
# MODULES
# =========================================================

@app.route("/api/modules", methods=["GET"])
def modules():

    if not authenticate():

        return jsonify({
            "success": False,
            "error": "Authentication required."
        }), 401

    try:

        return jsonify({
            "success": True,
            "modules": eon.router.get_available_modules()
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# =========================================================
# SERVER
# =========================================================

if __name__ == "__main__":

    port = int(
        os.getenv(
            "PORT",
            "10000"
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
