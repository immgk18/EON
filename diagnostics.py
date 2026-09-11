"""
EON Diagnostics
===============
Health monitoring, component checks and safe recovery support.
"""

import time
import traceback


class Diagnostics:
    """Monitors EON components and records system health."""

    def __init__(self, eon=None):
        self.eon = eon
        self.started_at = time.time()

        self.checks = {}
        self.errors = []
        self.recoveries = []

    # =========================================================
    # COMPONENT CHECK
    # =========================================================

    def check_component(self, name, component):
        """Check whether a component is available."""

        if component is None:

            result = {
                "component": name,
                "status": "OFFLINE",
                "healthy": False,
            }

            self.checks[name] = result

            return result

        try:

            status_method = getattr(
                component,
                "status",
                None
            )

            if callable(status_method):

                status = status_method()

                result = {
                    "component": name,
                    "status": "ONLINE",
                    "healthy": True,
                    "details": status,
                }

            else:

                result = {
                    "component": name,
                    "status": "AVAILABLE",
                    "healthy": True,
                }

        except Exception as error:

            result = {
                "component": name,
                "status": "ERROR",
                "healthy": False,
                "error": str(error),
            }

            self.record_error(
                name,
                error
            )

        self.checks[name] = result

        return result

    # =========================================================
    # FULL SYSTEM CHECK
    # =========================================================

    def run_health_check(self):

        if self.eon is None:

            return {
                "healthy": False,
                "status": "NO_EON",
                "components": {},
            }

        components = {

            "context":
                self.eon.context,

            "router":
                self.eon.router,

            "security":
                self.eon.security,

            "memory":
                self.eon.memory,

            "tasks":
                self.eon.tasks,

            "agents":
                self.eon.agents,

            "files":
                self.eon.files,

            "web":
                self.eon.web,

            "tools":
                self.eon.tools,

            "brain":
                self.eon.brain,

            "computer":
                self.eon.computer,

            "vision":
                self.eon.vision,

            "voice":
                self.eon.voice,

            "ui":
                self.eon.ui,
        }

        results = {}

        healthy_count = 0

        for name, component in components.items():

            result = self.check_component(
                name,
                component
            )

            results[name] = result

            if result.get(
                "healthy",
                False
            ):

                healthy_count += 1

        total = len(components)

        overall = (
            healthy_count == total
        )

        return {

            "healthy":
                overall,

            "status":
                "HEALTHY"
                if overall
                else "DEGRADED",

            "healthy_components":
                healthy_count,

            "total_components":
                total,

            "components":
                results,
        }

    # =========================================================
    # ERROR LOGGING
    # =========================================================

    def record_error(
        self,
        component,
        error
    ):

        entry = {

            "timestamp":
                time.time(),

            "component":
                component,

            "error":
                str(error),

        }

        self.errors.append(
            entry
        )

        # Keep memory usage bounded.

        if len(self.errors) > 100:

            self.errors = (
                self.errors[-100:]
            )

        return entry

    # =========================================================
    # SAFE EXECUTION
    # =========================================================

    def safe_execute(
        self,
        component,
        operation,
        fallback=None
    ):
        """
        Execute an operation safely.

        If it fails, record the error and
        return the supplied fallback.
        """

        try:

            return operation()

        except Exception as error:

            self.record_error(
                component,
                error
            )

            return fallback

    # =========================================================
    # RECOVERY
    # =========================================================

    def recover_component(
        self,
        name,
        component
    ):

        if component is None:

            return False

        try:

            reset_method = getattr(
                component,
                "reset",
                None
            )

            if callable(reset_method):

                reset_method()

                self.recoveries.append({

                    "timestamp":
                        time.time(),

                    "component":
                        name,

                    "action":
                        "reset",

                    "success":
                        True,
                })

                return True

            reconnect_method = getattr(
                component,
                "connect",
                None
            )

            if callable(reconnect_method):

                success = (
                    reconnect_method()
                )

                self.recoveries.append({

                    "timestamp":
                        time.time(),

                    "component":
                        name,

                    "action":
                        "reconnect",

                    "success":
                        bool(success),
                })

                return bool(success)

        except Exception as error:

            self.record_error(
                name,
                error
            )

        return False

    # =========================================================
    # SYSTEM STATUS
    # =========================================================

    def status(self):

        uptime = (
            time.time()
            - self.started_at
        )

        return {

            "status":
                "ONLINE",

            "uptime_seconds":
                round(
                    uptime,
                    2
                ),

            "checks":
                len(self.checks),

            "errors":
                len(self.errors),

            "recoveries":
                len(self.recoveries),
        }

    # =========================================================
    # ERROR HISTORY
    # =========================================================

    def get_errors(self):

        return self.errors.copy()

    def get_recoveries(self):

        return self.recoveries.copy()

    # =========================================================
    # RESET DIAGNOSTICS
    # =========================================================

    def clear_logs(self):

        self.errors.clear()
        self.recoveries.clear()

        return True
