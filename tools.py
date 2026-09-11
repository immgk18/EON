"""
EON Tool System
===============
Central registry and execution layer for EON tools.

The Tool System provides controlled capabilities that EON
can call when processing a request.

Built-in tools:
- Calculator
- System information
- File listing
- File reading
- Web search URL
- Task creation
"""


import ast
import operator
import platform
from urllib.parse import quote


# =============================================================
# SAFE CALCULATOR
# =============================================================

class SafeCalculator:
    """Performs basic mathematical calculations safely."""

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def calculate(self, expression):
        """Evaluate a basic mathematical expression safely."""

        if not expression:
            return "No expression provided."

        try:
            tree = ast.parse(
                expression,
                mode="eval"
            )

            result = self._evaluate(
                tree.body
            )

            return str(result)

        except (
            ValueError,
            TypeError,
            ZeroDivisionError,
            SyntaxError,
            OverflowError,
        ) as error:

            return f"Calculation error: {error}"

    def _evaluate(self, node):

        if isinstance(node, ast.Constant):

            if isinstance(
                node.value,
                (int, float)
            ):
                return node.value

            raise ValueError(
                "Only numbers are allowed."
            )

        if isinstance(node, ast.BinOp):

            operator_function = self.OPERATORS.get(
                type(node.op)
            )

            if operator_function is None:
                raise ValueError(
                    "Operator not supported."
                )

            left = self._evaluate(
                node.left
            )

            right = self._evaluate(
                node.right
            )

            return operator_function(
                left,
                right
            )

        if isinstance(node, ast.UnaryOp):

            operator_function = self.OPERATORS.get(
                type(node.op)
            )

            if operator_function is None:
                raise ValueError(
                    "Unary operator not supported."
                )

            value = self._evaluate(
                node.operand
            )

            return operator_function(
                value
            )

        raise ValueError(
            "Invalid mathematical expression."
        )


# =============================================================
# TOOL
# =============================================================

class Tool:
    """Represents a single EON tool."""

    def __init__(
        self,
        name,
        description,
        function=None
    ):

        self.name = name
        self.description = description
        self.function = function
        self.enabled = True

    def execute(self, *args, **kwargs):
        """Execute the registered tool."""

        if not self.enabled:
            return (
                f"Tool '{self.name}' "
                "is disabled."
            )

        if self.function is None:
            return (
                f"Tool '{self.name}' "
                "has no implementation."
            )

        try:

            return self.function(
                *args,
                **kwargs
            )

        except Exception as error:

            return (
                f"Tool '{self.name}' "
                f"failed: {error}"
            )


# =============================================================
# TOOL REGISTRY
# =============================================================

class ToolRegistry:
    """
    Central registry for EON tools.

    Tools can be registered, removed, enabled,
    disabled, and executed through this class.
    """

    def __init__(
        self,
        file_manager=None,
        task_engine=None,
        web_manager=None,
        security=None,
    ):

        self.tools = {}

        self.file_manager = file_manager
        self.task_engine = task_engine
        self.web_manager = web_manager
        self.security = security

        self.calculator = SafeCalculator()

        self.register_core_tools()

    # =========================================================
    # CORE TOOLS
    # =========================================================

    def register_core_tools(self):

        # -----------------------------------------------------
        # CALCULATOR
        # -----------------------------------------------------

        self.register(
            name="calculator",
            description=(
                "Performs safe mathematical calculations."
            ),
            function=self.calculate,
        )

        # -----------------------------------------------------
        # SYSTEM INFO
        # -----------------------------------------------------

        self.register(
            name="system_info",
            description=(
                "Retrieves basic computer information."
            ),
            function=self.system_info,
        )

        # -----------------------------------------------------
        # FILE LISTING
        # -----------------------------------------------------

        self.register(
            name="file_list",
            description=(
                "Lists files inside the approved "
                "EON file area."
            ),
            function=self.list_files,
        )

        # -----------------------------------------------------
        # FILE READER
        # -----------------------------------------------------

        self.register(
            name="file_reader",
            description=(
                "Reads supported text files."
            ),
            function=self.read_file,
        )

        # -----------------------------------------------------
        # WEB SEARCH
        # -----------------------------------------------------

        self.register(
            name="web_search",
            description=(
                "Creates a web search request."
            ),
            function=self.web_search,
        )

        # -----------------------------------------------------
        # TASK CREATOR
        # -----------------------------------------------------

        self.register(
            name="task_creator",
            description=(
                "Creates a new EON task."
            ),
            function=self.create_task,
        )

    # =========================================================
    # REGISTER
    # =========================================================

    def register(
        self,
        name,
        description,
        function=None
    ):

        if not name:
            return False

        if name in self.tools:
            return False

        self.tools[name] = Tool(
            name=name,
            description=description,
            function=function,
        )

        return True

    # =========================================================
    # UNREGISTER
    # =========================================================

    def unregister(self, name):

        if name not in self.tools:
            return False

        del self.tools[name]

        return True

    # =========================================================
    # GET
    # =========================================================

    def get(self, name):

        return self.tools.get(
            name
        )

    # =========================================================
    # EXECUTE
    # =========================================================

    def execute(
        self,
        name,
        *args,
        **kwargs
    ):

        tool = self.get(
            name
        )

        if tool is None:

            return (
                f"Tool '{name}' "
                "was not found."
            )

        return tool.execute(
            *args,
            **kwargs
        )

    # =========================================================
    # ENABLE
    # =========================================================

    def enable(self, name):

        tool = self.get(
            name
        )

        if tool is None:
            return False

        tool.enabled = True

        return True

    # =========================================================
    # DISABLE
    # =========================================================

    def disable(self, name):

        tool = self.get(
            name
        )

        if tool is None:
            return False

        tool.enabled = False

        return True

    # =========================================================
    # LIST TOOLS
    # =========================================================

    def list_tools(self):

        return list(
            self.tools.values()
        )

    # =========================================================
    # TOOL NAMES
    # =========================================================

    def get_tool_names(self):

        return list(
            self.tools.keys()
        )

    # =========================================================
    # TOOL DESCRIPTIONS
    # =========================================================

    def get_tool_descriptions(self):

        return {
            name: tool.description
            for name, tool in self.tools.items()
        }

    # =========================================================
    # CALCULATOR
    # =========================================================

    def calculate(self, expression):

        return self.calculator.calculate(
            expression
        )

    # =========================================================
    # SYSTEM INFORMATION
    # =========================================================

    def system_info(self):

        return {
            "operating_system":
                platform.system(),

            "os_version":
                platform.version(),

            "machine":
                platform.machine(),

            "processor":
                platform.processor(),

            "python":
                platform.python_version(),
        }

    # =========================================================
    # FILE LIST
    # =========================================================

    def list_files(self, path="."):

        if self.file_manager is None:

            return (
                "File manager is not connected."
            )

        return self.file_manager.list_files(
            path
        )

    # =========================================================
    # FILE READER
    # =========================================================

    def read_file(self, path):

        if self.file_manager is None:

            return (
                "File manager is not connected."
            )

        return self.file_manager.read_file(
            path
        )

    # =========================================================
    # WEB SEARCH
    # =========================================================

    def web_search(self, query):

        if not query:

            return (
                "No search query provided."
            )

        if self.web_manager:

            return self.web_manager.create_search_url(
                query
            )

        encoded_query = quote(
            query
        )

        return (
            "https://www.google.com/search?q="
            f"{encoded_query}"
        )

    # =========================================================
    # CREATE TASK
    # =========================================================

    def create_task(
        self,
        title,
        description=""
    ):

        if self.task_engine is None:

            return (
                "Task engine is not connected."
            )

        if not title:

            return (
                "No task title provided."
            )

        task = self.task_engine.create_task(
            title,
            description
        )

        return {
            "task_id":
                task.task_id,

            "title":
                task.title,

            "status":
                task.status,
        }

    # =========================================================
    # STATUS
    # =========================================================

    def status(self):

        total = len(
            self.tools
        )

        enabled = sum(
            1
            for tool in self.tools.values()
            if tool.enabled
        )

        return {
            "status":
                "ONLINE",

            "total_tools":
                total,

            "enabled_tools":
                enabled,

            "disabled_tools":
                total - enabled,

            "tools":
                self.get_tool_names(),
        }
