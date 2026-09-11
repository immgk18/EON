"""
EON Brain
=========
Reasoning and decision layer of EON.

The AI model can be connected to this layer later.
"""

from typing import Optional


class Brain:
    """EON's central reasoning interface."""

    def __init__(self, context):
        self.context = context
        self.name = "EON Brain"
        self.status = "READY"

    def think(self, command: str) -> str:
        """
        Process a user command and generate a response.

        The current version uses basic local reasoning.
        A real AI model can be connected here later.
        """

        if not command:
            return "I didn't receive a command."

        command = command.strip()
        lowered = command.lower()

        # Basic identity
        if lowered in {"hi", "hello", "hey"}:
            return "Hello. EON is online and ready."

        if "who are you" in lowered:
            return (
                "I am EON — Executive Orchestration Network, "
                "your personal AI computing system."
            )

        # System status
        if lowered == "status" or "system status" in lowered:
            return self.system_status()

        # Help
        if lowered in {"help", "what can you do"}:
            return self.help()

        # Context information
        if "history" in lowered:
            return self.history_summary()

        # Default response
        return (
            f"I understand your command: '{command}'. "
            "The reasoning engine is ready for deeper AI integration."
        )

    def system_status(self) -> str:
        """Return the current brain status."""

        history_count = len(self.context.get_history())

        return (
            "EON systems are operational. "
            f"Brain: {self.status}. "
            f"Context messages: {history_count}."
        )

    def help(self) -> str:
        """Return basic EON capabilities."""

        return (
            "I can understand commands, maintain context, "
            "route requests to EON modules, and coordinate tasks. "
            "Voice, vision, web, computer control, memory, "
            "and advanced AI reasoning will connect through "
            "their respective modules."
        )

    def history_summary(self) -> str:
        """Return a simple summary of the current session."""

        history = self.context.get_history()

        if not history:
            return "There is no conversation history yet."

        return f"This session currently contains {len(history)} messages."

    def reset(self) -> None:
        """Reset the brain's current context."""

        self.context.clear()
