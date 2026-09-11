"""
EON API
=======
Network interface for EON.

The API allows authorized clients such as:
- Mobile UI
- Web UI
- Desktop UI

to communicate with EON Core.

Security principles:
- Authentication token
- Controlled endpoints
- No unrestricted command execution
- Sensitive operations remain under EON Security
"""

import secrets
from functools import wraps

from flask import Flask, jsonify, request

from config import Config


class EONAPI:
    """HTTP API interface for EON."""

    def __init__(self, eon):

        self.eon = eon

        self.app = Flask(
            "EON API"
        )

        # -----------------------------------------------------
        # API token
        # -----------------------------------------------------

        self.api_token = secrets.token_urlsafe(
            32
        )

        self._register_routes()

    # =========================================================
    # AUTHENTICATION
    # =========================================================

    def _authorized(self):

        token = request.headers.get(
            "X-EON-Token"
        )

        if not token:

            return False

        return secrets.compare_digest(
            token,
            self.api_token
        )

    def _require_auth(
        self,
        function
    ):

        @wraps(function)
        def wrapper(*args, **kwargs):

            if not self._authorized():

                return jsonify({
                    "success": False,
                    "error":
                        "Authentication required.",
                }), 401

            return function(
                *args,
                **kwargs
            )

        return wrapper

    # =========================================================
    # ROUTES
    # =========================================================

    def _register_routes(self):

        self.app.add_url_rule(
            "/api",
            "api_info",
            self.api_info,
            methods=["GET"]
        )

        self.app.add_url_rule(
            "/api/status",
            "status",
            self.status,
            methods=["GET"]
        )

        self.app.add_url_rule(
            "/api/command",
            "command",
            self.command,
            methods=["POST"]
        )

        self.app.add_url_rule(
            "/api/tasks",
            "tasks",
            self.tasks,
            methods=["GET"]
        )

        self.app.add_url_rule(
            "/api/memory",
            "memory",
            self.memory,
            methods=["GET"]
        )

    # =========================================================
    # API INFORMATION
    # =========================================================

    def api_info(self):

        return jsonify({

            "name":
                "EON API",

            "version":
                "1.0",

            "system":
                "Executive Orchestration Network",

            "status":
                "ONLINE",

            "authentication":
                "TOKEN_REQUIRED",
        })

    # =========================================================
    # STATUS
    # =========================================================

    def status(self):

        if not self._authorized():

            return jsonify({
                "success": False,
                "error":
                    "Authentication required.",
            }), 401

        return jsonify({
            "success": True,
            "eon": self.eon.status(),
        })

    # =========================================================
    # COMMAND
    # =========================================================

    def command(self):

        if not self._authorized():

            return jsonify({
                "success": False,
                "error":
                    "Authentication required.",
            }), 401

        data = request.get_json(
            silent=True
        )

        if not isinstance(
            data,
            dict
        ):

            return jsonify({
                "success": False,
                "error":
                    "JSON request body required.",
            }), 400

        command = data.get(
            "command"
        )

        if not isinstance(
            command,
            str
        ):

            return jsonify({
                "success": False,
                "error":
                    "Command must be text.",
            }), 400

        command = command.strip()

        if not command:

            return jsonify({
                "success": False,
                "error":
                    "Command cannot be empty.",
            }), 400

        # -----------------------------------------------------
        # Central EON processing
        # -----------------------------------------------------

        try:

            response = (
                self.eon.handle_command(
                    command
                )
            )

            return jsonify({

                "success":
                    True,

                "command":
                    command,

                "response":
                    response,

                "module":
                    self.eon.context.get_module(),
            })

        except Exception as error:

            return jsonify({

                "success":
                    False,

                "error":
                    str(error),
            }), 500

    # =========================================================
    # TASKS
    # =========================================================

    def tasks(self):

        if not self._authorized():

            return jsonify({
                "success": False,
                "error":
                    "Authentication required.",
            }), 401

        task_list = (
            self.eon.tasks.list_tasks()
        )

        result = []

        for task in task_list:

            result.append({

                "id":
                    task.task_id,

                "title":
                    task.title,

                "status":
                    task.status,
            })

        return jsonify({

            "success":
                True,

            "tasks":
                result,
        })

    # =========================================================
    # MEMORY
    # =========================================================

    def memory(self):

        if not self._authorized():

            return jsonify({
                "success": False,
                "error":
                    "Authentication required.",
            }), 401

        memories = (
            self.eon.memory.recall()
        )

        result = []

        for memory in memories:

            result.append({

                "id":
                    memory[0],

                "category":
                    memory[1],

                "content":
                    memory[2],

                "created_at":
                    memory[3],
            })

        return jsonify({

            "success":
                True,

            "memories":
                result,
        })

    # =========================================================
    # RUN SERVER
    # =========================================================

    def run(
        self,
        host=None,
        port=None,
        debug=None
    ):

        host = (
            host
            or Config.HOST
        )

        port = (
            port
            or Config.PORT
        )

        if debug is None:

            debug = Config.DEBUG

        self.app.run(
            host=host,
            port=port,
            debug=debug,
        )
