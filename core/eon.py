"""
EON Context
===========
Maintains conversation and active-task context.
"""


class Context:
    """Stores EON's active session context."""

    def __init__(self):
        self.history = []
        self.current_task = None
        self.current_goal = None
        self.active_module = None
        self.variables = {}

    # ─────────────────────────────────────
    # MESSAGE HISTORY
    # ─────────────────────────────────────

    def add_message(self, role, message):
        """Add a message to the current session."""

        self.history.append({
            "role": role,
            "message": message
        })

    def get_history(self):
        """Return the complete conversation history."""

        return self.history.copy()

    def get_recent(self, count=10):
        """Return the most recent messages."""

        if count <= 0:
            return []

        return self.history[-count:]

    # ─────────────────────────────────────
    # GOAL
    # ─────────────────────────────────────

    def set_goal(self, goal):
        """Set the current goal."""

        self.current_goal = goal

    def get_goal(self):
        """Return the current goal."""

        return self.current_goal

    # ─────────────────────────────────────
    # TASK
    # ─────────────────────────────────────

    def set_task(self, task):
        """Set the currently active task."""

        self.current_task = task

    def get_task(self):
        """Return the active task."""

        return self.current_task

    # ─────────────────────────────────────
    # MODULE
    # ─────────────────────────────────────

    def set_module(self, module):
        """Set the currently active EON module."""

        self.active_module = module

    def get_module(self):
        """Return the active module."""

        return self.active_module

    # ─────────────────────────────────────
    # VARIABLES
    # ─────────────────────────────────────

    def set_variable(self, name, value):
        """Store a temporary session variable."""

        if name:
            self.variables[name] = value

    def get_variable(self, name, default=None):
        """Retrieve a session variable."""

        return self.variables.get(
            name,
            default
        )

    def remove_variable(self, name):
        """Remove a session variable."""

        if name in self.variables:
            del self.variables[name]
            return True

        return False

    # ─────────────────────────────────────
    # RESET
    # ─────────────────────────────────────

    def clear(self):
        """Clear the current session context."""

        self.history.clear()
        self.current_task = None
        self.current_goal = None
        self.active_module = None
        self.variables.clear()

    # ─────────────────────────────────────
    # STATUS
    # ─────────────────────────────────────

    def status(self):
        """Return context status."""

        return {
            "messages": len(self.history),
            "current_goal": self.current_goal,
            "current_task": self.current_task,
            "active_module": self.active_module,
            "variables": len(self.variables),
            "status": "ONLINE",
        }
