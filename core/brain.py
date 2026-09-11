"""
EON Brain
=========
Central reasoning and AI coordination layer for EON.
"""

from datetime import datetime

from config import Config
from ai_provider import AIProviderManager


class Brain:
    """Central reasoning engine for EON."""

    def __init__(
        self,
        context,
        tools=None,
        memory=None,
        agents=None,
        tasks=None
    ):
        self.context = context
        self.tools = tools
        self.memory = memory
        self.agents = agents
        self.tasks = tasks

        self.name = "EON Brain"
        self.status = "READY"

        self.provider_name = Config.AI_PROVIDER
        self.model = Config.AI_MODEL
        self.temperature = Config.AI_TEMPERATURE
        self.max_tokens = Config.AI_MAX_TOKENS

        self.ai = AIProviderManager(
            provider=self.provider_name,
            model=self.model
        )

        self.system_role = (
            "You are EON, Executive Orchestration Network. "
            "You are a personal AI computing system. "
            "Understand requests, maintain context, "
            "reason about problems, plan tasks, and "
            "coordinate available EON capabilities. "
            "Be useful, clear, concise, and honest."
        )

    # =========================================================
    # THINK
    # =========================================================

    def think(self, command):

        if not command:
            return "I didn't receive a command."

        command = command.strip()
        lowered = command.lower()

        if lowered in {"hi", "hello", "hey"}:
            return "Hello. EON is online and ready."

        if "who are you" in lowered:
            return (
                "I am EON — Executive Orchestration Network, "
                "your personal AI computing system."
            )

        if lowered == "status":
            return self.system_status()

        if lowered in {"help", "what can you do"}:
            return self.help()

        if "time" in lowered:
            return self.current_time()

        if "history" in lowered:
            return self.history_summary()

        self.context.add_message(
            "brain",
            command
        )

        # -----------------------------------------------------
        # Try EON tools first
        # -----------------------------------------------------

        tool_result = self.detect_and_use_tool(
            command
        )

        if tool_result is not None:
            return tool_result

        # -----------------------------------------------------
        # Send remaining request to AI
        # -----------------------------------------------------

        ai_response = self.ask_ai(
            command
        )

        if ai_response:
            return ai_response

        return self.general_reasoning(
            command
        )

    # =========================================================
    # TOOL DETECTION
    # =========================================================

    def detect_and_use_tool(self, command):

        lowered = command.lower()

        if (
            "calculate" in lowered
            or "what is" in lowered
            or "solve" in lowered
        ):
            expression = (
                self.extract_math_expression(
                    command
                )
            )

            if expression:
                return self.execute_tool(
                    "calculator",
                    expression
                )

        if (
            "system information" in lowered
            or "system info" in lowered
            or "computer information" in lowered
        ):
            return self.execute_tool(
                "system_info"
            )

        if (
            "list files" in lowered
            or "show files" in lowered
            or "my files" in lowered
        ):
            result = self.execute_tool(
                "file_list"
            )

            return self.format_tool_result(
                result
            )

        if (
            lowered.startswith("search ")
            or lowered.startswith("search the web ")
            or "search online" in lowered
        ):
            query = self.extract_search_query(
                command
            )

            if query:
                result = self.execute_tool(
                    "web_search",
                    query
                )

                return (
                    f"Search prepared for: "
                    f"{query}\n{result}"
                )

        if (
            "create task" in lowered
            or "add task" in lowered
            or "make a task" in lowered
        ):
            title = self.extract_task_title(
                command
            )

            result = self.execute_tool(
                "task_creator",
                title
            )

            return self.format_tool_result(
                result
            )

        return None

    # =========================================================
    # TOOL EXECUTION
    # =========================================================

    def execute_tool(
        self,
        tool_name,
        *args,
        **kwargs
    ):

        if self.tools is None:
            return "Tool system is not connected."

        return self.tools.execute(
            tool_name,
            *args,
            **kwargs
        )

    # =========================================================
    # AI REQUEST
    # =========================================================

    def ask_ai(self, command):

        prompt = self._build_prompt(
            command
        )

        return self.ai.generate(
            prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

    # =========================================================
    # PROMPT BUILDER
    # =========================================================

    def _build_prompt(self, command):

        recent_history = (
            self.context.get_recent(8)
        )

        history_text = []

        for message in recent_history:

            role = message.get(
                "role",
                "unknown"
            )

            content = message.get(
                "message",
                ""
            )

            history_text.append(
                f"{role.upper()}: {content}"
            )

        history = "\n".join(
            history_text
        )

        memory_text = ""

        if self.memory is not None:

            try:

                relevant = (
                    self.memory.relevant(
                        command,
                        limit=3
                    )
                )

                if relevant:

                    memory_lines = []

                    for item in relevant:

                        memory_lines.append(
                            f"- {item[2]}"
                        )

                    memory_text = (
                        "\nRELEVANT MEMORY:\n"
                        + "\n".join(
                            memory_lines
                        )
                    )

            except Exception:

                memory_text = ""

        return (
            f"SYSTEM:\n"
            f"{self.system_role}\n\n"

            f"RECENT CONTEXT:\n"
            f"{history}\n"

            f"{memory_text}\n\n"

            f"USER:\n"
            f"{command}\n\n"

            f"EON:"
        )

    # =========================================================
    # MATH
    # =========================================================

    def extract_math_expression(
        self,
        command
    ):

        text = command.lower()

        prefixes = [
            "calculate",
            "what is",
            "solve",
            "compute",
        ]

        for prefix in prefixes:

            if text.startswith(prefix):

                expression = (
                    command[
                        len(prefix):
                    ].strip()
                )

                expression = (
                    expression
                    .replace("×", "*")
                    .replace("÷", "/")
                )

                if self.is_safe_math(
                    expression
                ):
                    return expression

        return None

    def is_safe_math(
        self,
        expression
    ):

        if not expression:
            return False

        allowed = set(
            "0123456789+-*/().% "
        )

        return all(
            character in allowed
            for character in expression
        )

    # =========================================================
    # SEARCH
    # =========================================================

    def extract_search_query(
        self,
        command
    ):

        lowered = command.lower()

        prefixes = [
            "search the web",
            "search online",
            "search",
        ]

        for prefix in prefixes:

            if lowered.startswith(prefix):

                return (
                    command[
                        len(prefix):
                    ].strip()
                )

        return None

    # =========================================================
    # TASK
    # =========================================================

    def extract_task_title(
        self,
        command
    ):

        lowered = command.lower()

        prefixes = [
            "create task",
            "add task",
            "make a task",
        ]

        for prefix in prefixes:

            if lowered.startswith(prefix):

                title = (
                    command[
                        len(prefix):
                    ].strip()
                )

                if title:
                    return title

        return command

    # =========================================================
    # FORMAT TOOL RESULT
    # =========================================================

    def format_tool_result(
        self,
        result
    ):

        if isinstance(result, dict):

            return "\n".join(
                f"{key}: {value}"
                for key, value
                in result.items()
            )

        if isinstance(result, list):

            if not result:
                return "No results found."

            return "\n".join(
                f"- {item}"
                for item in result
            )

        return str(result)

    # =========================================================
    # STATUS
    # =========================================================

    def system_status(self):

        history_count = len(
            self.context.get_history()
        )

        ai_status = self.ai.status()

        return (
            "EON systems are operational.\n"
            f"Brain: {self.status}.\n"
            f"AI Provider: "
            f"{ai_status.get('provider')}.\n"
            f"AI Model: "
            f"{ai_status.get('model') or 'None'}.\n"
            f"AI Status: "
            f"{ai_status.get('status')}.\n"
            f"Tools: "
            f"{'CONNECTED' if self.tools else 'NOT CONNECTED'}.\n"
            f"Context messages: "
            f"{history_count}."
        )

    # =========================================================
    # HELP
    # =========================================================

    def help(self):

        return (
            "I can understand requests, maintain context, "
            "use tools, perform calculations, inspect files, "
            "create tasks, prepare web searches, coordinate "
            "agents, process visual input, use memory, and "
            "interact through voice."
        )

    # =========================================================
    # TIME
    # =========================================================

    def current_time(self):

        now = datetime.now()

        return (
            "The current local time is "
            f"{now.strftime('%I:%M:%S %p')}."
        )

    # =========================================================
    # HISTORY
    # =========================================================

    def history_summary(self):

        history = (
            self.context.get_history()
        )

        if not history:

            return (
                "There is no conversation history yet."
            )

        return (
            "This session currently contains "
            f"{len(history)} messages."
        )

    # =========================================================
    # FALLBACK
    # =========================================================

    def general_reasoning(
        self,
        command
    ):

        return (
            f"I understand your request: "
            f"'{command}'\n"
            "The EON reasoning interface is ready, "
            "but no AI model is currently available."
        )

    # =========================================================
    # RESET
    # =========================================================

    def reset(self):

        self.context.clear()

        return (
            "EON Brain context has been reset."
        )
