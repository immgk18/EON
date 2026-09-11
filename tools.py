"""
EON Tool System
===============
Central registry for EON capabilities.
"""


class Tool:
    """Represents a single tool available to EON."""

    def __init__(self, name, description, function=None):
        self.name = name
        self.description = description
        self.function = function
        self.enabled = True

    def execute(self, *args, **kwargs):
        """Execute the tool."""

        if not self.enabled:
            return f"Tool '{self.name}' is disabled."

        if self.function is None:
            return (
                f"Tool '{self.name}' is registered "
                "but has no implementation yet."
            )

        return self.function(*args, **kwargs)


class ToolRegistry:
    """Central registry for EON tools."""

    def __init__(self):
        self.tools = {}

        self.register_core_tools()

    def register_core_tools(self):
        """Register EON's initial tool interfaces."""

        self.register(
            "calculator",
            "Performs mathematical calculations."
        )

        self.register(
            "web_search",
            "Searches the web for information."
        )

        self.register(
            "file_reader",
            "Reads supported files."
        )

        self.register(
            "image_analyzer",
            "Analyzes images using the vision system."
        )

        self.register(
            "system_info",
            "Retrieves basic computer information."
        )

        self.register(
            "task_manager",
            "Creates and manages EON tasks."
        )

    def register(self, name, description, function=None):
        """Register a new tool."""

        if not name:
            return False

        self.tools[name] = Tool(
            name=name,
            description=description,
            function=function
        )

        return True

    def unregister(self, name):
        """Remove a tool."""

        if name not in self.tools:
            return False

        del self.tools[name]
        return True

    def get(self, name):
        """Retrieve a tool."""

        return self.tools.get(name)

    def execute(self, name, *args, **kwargs):
        """Execute a registered tool."""

        tool = self.get(name)

        if tool is None:
            return f"Tool '{name}' was not found."

        return tool.execute(*args, **kwargs)

    def enable(self, name):
        """Enable a tool."""

        tool = self.get(name)

        if tool is None:
            return False

        tool.enabled = True
        return True

    def disable(self, name):
        """Disable a tool."""

        tool = self.get(name)

        if tool is None:
            return False

        tool.enabled = False
        return True

    def list_tools(self):
        """Return all registered tools."""

        return list(self.tools.values())

    def get_tool_names(self):
        """Return tool names."""

        return list(self.tools.keys())

    def status(self):
        """Return tool registry status."""

        total = len(self.tools)

        enabled = sum(
            1
            for tool in self.tools.values()
            if tool.enabled
        )

        return {
            "status": "ONLINE",
            "total_tools": total,
            "enabled_tools": enabled,
            "disabled_tools": total - enabled,
        }
