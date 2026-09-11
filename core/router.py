"""
EON Router
==========
Determines which EON subsystem should handle a command.
"""


class Router:
    """EON's command routing system."""

    def __init__(self):
        self.routes = {
            "voice": [
                "voice",
                "speak",
                "listen",
                "say",
                "hear",
            ],

            "vision": [
                "image",
                "picture",
                "photo",
                "screen",
                "see",
                "look",
                "visual",
            ],

            "web": [
                "search",
                "internet",
                "web",
                "online",
                "latest",
                "news",
                "weather",
            ],

            "computer": [
                "computer",
                "desktop",
                "application",
                "app",
                "open",
                "close",
                "launch",
            ],

            "memory": [
                "remember",
                "memory",
                "recall",
                "forget",
            ],

            "tasks": [
                "task",
                "plan",
                "schedule",
                "todo",
                "remind",
            ],

            "files": [
                "file",
                "folder",
                "document",
                "pdf",
                "read file",
            ],

            "agents": [
                "agent",
                "research",
                "analyze",
                "analysis",
                "coding",
            ],
        }

    def route(self, command: str) -> str:
        """
        Determine the most suitable module for a command.
        """

        if not command:
            return "brain"

        command_lower = command.lower()

        # Check every registered module
        for module, keywords in self.routes.items():

            for keyword in keywords:

                if keyword in command_lower:
                    return module

        # If no specific module matches,
        # send the request to EON's brain.
        return "brain"

    def get_available_modules(self):
        """Return all registered EON modules."""

        return list(self.routes.keys())

    def add_route(self, module: str, keywords: list):
        """Add a new module to the routing system."""

        if not module:
            return

        self.routes[module] = keywords

    def remove_route(self, module: str):
        """Remove a module from the routing system."""

        if module in self.routes:
            del self.routes[module]
