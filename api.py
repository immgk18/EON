"""
EON API
=======
Network interface for EON.

Provides:
- EON status
- Command processing
- Task information
- Memory information

Authentication is handled using an environment
variable so secrets are never hard-coded.
"""

import os
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

        # =====================================================
        # API AUTHENTICATION
        # =====================================================

        self.api_token = os.getenv(
            "EON_API_TOKEN",
            ""
        ).strip()

        self._register_routes()

    # =========================================================
    # AUTHENTICATION
    # =========================================================

    def _authorized(self):

        # No configured token = deny access.
        if not self.api_token:
            return False

        token = request.headers.get(
            "X-EON-Token",
            ""
        ).strip()

        if not token:
            return False

        try:

            return secrets.compare_digest(
                token,
                self.api_token
            )

        except TypeError:

            return False

    def _require_auth(self, function):
        """Protect an API endpoint with authentication."""

        @wraps(function)
        def wrapper(*args, **kwargs):

            if not self._authorized():

                return jsonify({
                    "success": False,
                    "error":
                        "Authentication required."
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

        # Public health endpoint
        self.app.add_url_rule(
            "/api",
            "api_info",
            self.api_info,
            methods=["GET"]
        )

        # Protected endpoints
        self.app.add_url_rule(
            "/api/status",
            "status",
            self._require_auth(
                self.status
            ),
            methods=["GET"]
        )

        self.app.add_url_rule(
            "/api/command",
            "command",
            self._require_auth(
                self.command
            ),
            methods=["POST"]
        )

        self.app.add_url_rule(
            "/api/tasks",
            "tasks",
            self._require_auth(
                self.tasks
            ),
            methods=["GET"]
        )

        self.app.add_url_rule(
            "/api/memory",
            "memory",
            self._require_auth(
                self.memory
            ),
            methods=["GET"]
        )

    # =========================================================
    # API INFORMATION
    # =========================================================

    def api_info(self):

        return jsonify({

            "success":
                True,

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

        try:

            eon_status = (
                self.eon.status()
            )

            return jsonify({

                "success":
                    True,

                "eon":
                    eon_status,

            })

        except Exception as error:

            return jsonify({

                "success":
                    False,

                "error":
                    str(error),

            }), 500

    # =========================================================
    # COMMAND
    # =========================================================

    def command(self):

        data = request.get_json(
            silent=True
        )

        if not isinstance(
            data,
            dict
        ):

            return jsonify({

                "success":
                    False,

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

                "success":
                    False,

                "error":
                    "Command must be text.",

            }), 400

        command = command.strip()

        if not command:

            return jsonify({

                "success":
                    False,

                "error":
                    "Command cannot be empty.",

            }), 400

        # Prevent unnecessarily huge requests.
        if len(command) > 2000:

            return jsonify({

                "success":
                    False,

                "error":
                    "Command is too long.",

            }), 413

        # =====================================================
        # SEND COMMAND TO EON CORE
        # =====================================================

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

            # Record the error if diagnostics exists.
            try:

                self.eon.diagnostics.record_error(
                    "api_command",
                    error
                )

            except Exception:

                pass

            return jsonify({

                "success":
                    False,

                "error":
                    "EON failed to process the command.",

            }), 500

    # =========================================================
    # TASKS
    # =========================================================

    def tasks(self):

        try:

            task_list = (
                self.eon.tasks.list_tasks()
            )

            result = []

            for task in task_list:

                # Support the current Task structure.
                task_id = getattr(
                    task,
                    "id",
                    getattr(
                        task,
                        "task_id",
                        None
                    )
                )

                title = getattr(
                    task,
                    "title",
                    ""
                )

                status = getattr(
                    task,
                    "status",
                    "UNKNOWN"
                )

                result.append({

                    "id":
                        task_id,

                    "title":
                        title,

                    "status":
                        status,

                })

            return jsonify({

                "success":
                    True,

                "tasks":
                    result,

            })

        except Exception as error:

            return jsonify({

                "success":
                    False,

                "error":
                    str(error),

            }), 500

    # =========================================================
    # MEMORY
    # =========================================================

    def memory(self):

        try:

            memories = (
                self.eon.memory.recall()
            )

            result = []

            for memory in memories:

                # Handle dictionary-based memory.
                if isinstance(
                    memory,
                    dict
                ):

                    result.append(memory)

                # Handle tuple/list-based memory.
                elif isinstance(
                    memory,
                    (tuple, list)
                ):

                    result.append({

                        "id":
                            memory[0]
                            if len(memory) > 0
                            else None,

                        "category":
                            memory[1]
                            if len(memory) > 1
                            else None,

                        "content":
                            memory[2]
                            if len(memory) > 2
                            else None,

                        "created_at":
                            memory[3]
                            if len(memory) > 3
                            else None,

                    })

                else:

                    result.append({
                        "content":
                            str(memory)
                    })

            return jsonify({

                "success":
                    True,

                "memories":
                    result,

            })

        except Exception as error:

            return jsonify({

                "success":
                    False,

                "error":
                    str(error),

            }), 500

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
            or os.getenv(
                "EON_API_HOST",
                "127.0.0.1"
            )
        )

        port = (
            port
            or int(
                os.getenv(
                    "PORT",
                    str(Config.PORT)
                )
            )
        )

        if debug is None:

            debug = Config.DEBUG

        self.app.run(
            host=host,
            port=port,
            debug=debug,
        )
