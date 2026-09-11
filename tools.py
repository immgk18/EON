"""
EON Tool System
===============
Central registry for EON's capabilities and tools.
"""


class Tool:
    """Represents a single EON tool."""

    def __init__(self, name, description, function=None):
        self.name = name
        self.description = description
        self.function = function
        self.enabled = True

    def execute(self, *args, **kwargs):
        """Execute the tool."""

        if not self.enabled:
            return "Tool is currently disabled."

        if self.function is None:
            return f"Tool '{self.name}' is not implemented yet."

        return self.function(*args, **kwargs)


class ToolRegistry:
    """Manages all tools available to EON."""

    def __init__(self):
        self.tools = {}

    def register(self, name, description, function=None):
        """Register a new tool."""

        if name in self.tools:
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
        """Get a registered tool."""

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
        """Return the names of all registered tools."""

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
            "total_tools": total,
            "enabled_tools": enabled,
            "disabled_tools": total - enabled,
        }
