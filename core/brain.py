"""
EON Brain
=========
Central reasoning and coordination layer.
"""

from datetime import datetime


class Brain:
    """EON's central reasoning engine."""

    def __init__(self, context):
        self.context = context

        self.name = "EON Brain"
        self.status = "READY"

        self.system_role = (
            "You are EON, Executive Orchestration Network. "
            "You understand user requests, maintain context, "
            "plan tasks, and coordinate available capabilities."
        )

    # ─────────────────────────────────────
    # MAIN REASONING
    # ─────────────────────────────────────

    def think(self, command):
        """Process a command and generate a response."""

        if not command:
            return "I didn't receive a command."

        command = command.strip()
        lowered = command.lower()

        # Store reasoning request
        self.context.add_message(
            "brain",
            command
        )

        # Identity
        if lowered in {
            "hi",
            "hello",
            "hey",
        }:
            return (
                "Hello. EON is online and ready."
            )

        if "who are you" in lowered:
            return (
                "I am EON — Executive Orchestration Network, "
                "your personal AI computing system."
            )

        # Status
        if lowered == "status":
            return self.system_status()

        # Help
        if lowered in {
            "help",
            "what can you do",
        }:
            return self.help()

        # Time
        if "time" in lowered:
            return self.current_time()

        # Context
        if "history" in lowered:
            return self.history_summary()

        # Basic planning
        if (
            "plan" in lowered
            or "how do i" in lowered
        ):
            return self.create_basic_plan(command)

        # Default reasoning response
        return self.general_reasoning(command)

    # ─────────────────────────────────────
    # SYSTEM STATUS
    # ─────────────────────────────────────

    def system_status(self):
        """Return brain status."""

        history_count = len(
            self.context.get_history()
        )

        return (
            "EON systems are operational. "
            f"Brain: {self.status}. "
            f"Context messages: {history_count}."
        )

    # ─────────────────────────────────────
    # HELP
    # ─────────────────────────────────────

    def help(self):
        """Describe EON capabilities."""

        return (
            "I can understand requests, maintain context, "
            "plan tasks, route commands, work with files, "
            "use tools, coordinate agents, process visual input, "
            "use web information, and interact through voice."
        )

    # ─────────────────────────────────────
    # TIME
    # ─────────────────────────────────────

    def current_time(self):
        """Return the current local time."""

        now = datetime.now()

        return (
            f"The current local time is "
            f"{now.strftime('%I:%M:%S %p')}."
        )

    # ─────────────────────────────────────
    # HISTORY
    # ─────────────────────────────────────

    def history_summary(self):
        """Return a summary of conversation context."""

        history = self.context.get_history()

        if not history:
            return (
                "There is no conversation history yet."
            )

        return (
            f"This session currently contains "
            f"{len(history)} messages."
        )

    # ─────────────────────────────────────
    # BASIC PLANNING
    # ─────────────────────────────────────

    def create_basic_plan(self, command):
        """Create a simple preliminary plan."""

        return (
            "I would approach this in these stages:\n"
            "1. Understand the objective.\n"
            "2. Break it into smaller tasks.\n"
            "3. Select the appropriate EON capabilities.\n"
            "4. Execute the approved steps.\n"
            "5. Verify the results.\n"
            "6. Report the outcome."
        )

    # ─────────────────────────────────────
    # GENERAL REASONING
    # ─────────────────────────────────────

    def general_reasoning(self, command):
        """
        Handle requests that do not match a built-in command.

        A real AI model will eventually replace this method.
        """

        return (
            f"I understand your request: "
            f"'{command}'\n"
            "The EON reasoning interface is ready for "
            "connection to the AI engine."
        )

    # ─────────────────────────────────────
    # RESET
    # ─────────────────────────────────────

    def reset(self):
        """Reset the current reasoning context."""

        self.context.clear()
