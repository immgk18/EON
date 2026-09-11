class Brain:
    """EON's reasoning layer."""

    def __init__(self, context):
        self.context = context

    def think(self, command):
        """
        Basic reasoning layer.
        The real AI model will be connected here later.
        """

        command = command.strip()

        if not command:
            return "I didn't receive a command."

        command_lower = command.lower()

        if command_lower in ["hello", "hi", "hey"]:
            return "Hello. EON is ready."

        if "who are you" in command_lower:
            return "I am EON — Executive Orchestration Network."

        if "status" in command_lower:
            return "All core systems are operational."

        if "help" in command_lower:
            return (
                "I can process commands, reason about tasks, "
                "route requests, and coordinate EON modules."
            )

        return f"I've received your command: {command}"
