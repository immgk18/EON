class Router:
    """Routes commands to the appropriate EON subsystem."""

    def __init__(self):
        self.routes = {
            "voice": ["speak", "listen", "voice"],
            "vision": ["image", "picture", "screen", "see"],
            "web": ["search", "internet", "web", "latest"],
            "computer": ["open", "close", "computer", "application"],
            "memory": ["remember", "memory", "recall"],
            "task": ["task", "plan", "schedule"],
        }

    def route(self, command):
        command_lower = command.lower()

        for module, keywords in self.routes.items():
            for keyword in keywords:
                if keyword in command_lower:
                    return module

        return "brain"
