"""
EON Router
==========
Intent-based routing layer for EON.
"""


class Router:
    """Routes user requests to the correct EON subsystem."""

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
                "screenshot",
                "screen",
                "see",
                "look",
                "visual",
                "analyze this image",
            ],

            "web": [
                "search",
                "internet",
                "web",
                "online",
                "latest",
                "news",
                "weather",
                "look up",
            ],

            "computer": [
                "computer",
                "desktop",
                "application",
                "app",
                "open",
                "launch",
                "close",
            ],

            "memory": [
                "remember",
                "memory",
                "recall",
                "forget",
                "what did i tell you",
            ],

            "tasks": [
                "task",
                "plan",
                "schedule",
                "todo",
                "remind",
                "organize",
            ],

            "files": [
                "file",
                "folder",
                "document",
                "pdf",
                "read file",
                "open file",
            ],

            "agents": [
                "agent",
                "research",
                "researcher",
                "coding",
                "code",
                "analyze",
                "analysis",
            ],

            "tools": [
                "calculator",
                "calculate",
                "tool",
            ],
        }

    def route(self, command):
        """Determine which subsystem should handle a command."""

        if not command:
            return "brain"

        command_lower = command.lower().strip()

        # Check for exact system commands first.
        if command_lower in {
            "hello",
            "hi",
            "hey",
            "status",
            "help",
            "who are you",
        }:
            return "brain"

        # Find the best matching module.
        matches = []

        for module, keywords in self.routes.items():

            for keyword in keywords:

                if keyword in command_lower:
                    matches.append(
                        (
                            len(keyword),
                            module
                        )
                    )

        if not matches:
            return "brain"

        # Prefer the most specific/longest matching phrase.
        matches.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return matches[0][1]

    def get_available_modules(self):
        """Return all registered routing modules."""

        return list(self.routes.keys())

    def get_keywords(self, module):
        """Return keywords associated with a module."""

        return self.routes.get(module, [])

    def add_route(self, module, keywords):
        """Add or update a module route."""

        if not module:
            return False

        if not isinstance(keywords, list):
            return False

        self.routes[module] = keywords

        return True

    def remove_route(self, module):
        """Remove a routing module."""

        if module not in self.routes:
            return False

        del self.routes[module]

        return True

    def status(self):
        """Return router status."""

        return {
            "status": "ONLINE",
            "modules": len(self.routes),
            "available_modules": self.get_available_modules(),
        }
