"""
EON Brain
=========
Central reasoning and AI coordination layer for EON.

The Brain:
- Understands user commands
- Maintains context
- Selects appropriate tools
- Executes safe tools
- Connects to a local AI provider
- Falls back safely when AI is unavailable
"""

import ast
import json
import operator
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from config import Config


class Brain:
    """EON's central reasoning engine."""

    def __init__(self, context, tools=None):

        self.context = context
        self.tools = tools

        self.name = "EON Brain"
        self.status = "READY"

        self.provider = Config.AI_PROVIDER
        self.model = Config.AI_MODEL
        self.temperature = Config.AI_TEMPERATURE
        self.max_tokens = Config.AI_MAX_TOKENS

        self.system_role = (
            "You are EON, Executive Orchestration Network. "
            "You are a personal AI computing system. "
            "Understand requests, maintain context, "
            "reason about problems, plan tasks, and coordinate "
            "available EON capabilities. "
            "Be useful, clear, concise, and honest."
        )

    # =========================================================
    # TOOL CONNECTION
    # =========================================================

    def set_tools(self, tools):
        """Connect the EON Tool Registry to the Brain."""

        self.tools = tools

    # =========================================================
    # MAIN THINKING INTERFACE
    # =========================================================

    def think(self, command):

        if not command:
            return "I didn't receive a command."

        command = command.strip()
        lowered = command.lower()

        # -----------------------------------------------------
        # BASIC COMMANDS
        # -----------------------------------------------------

        if lowered in {
            "hi",
            "hello",
            "hey"
        }:
            return "Hello. EON is online and ready."

        if "who are you" in lowered:
            return (
                "I am EON — Executive Orchestration Network, "
                "your personal AI computing system."
            )

        if lowered == "status":
            return self.system_status()

        if lowered in {
            "help",
            "what can you do"
        }:
            return self.help()

        if "time" in lowered:
            return self.current_time()

        if "history" in lowered:
            return self.history_summary()

        # -----------------------------------------------------
        # SAVE USER COMMAND
        # -----------------------------------------------------

        self.context.add_message(
            "brain",
            command
        )

        # -----------------------------------------------------
        # TOOL DETECTION
        # -----------------------------------------------------

        tool_result = self.detect_and_use_tool(
            command
        )

        if tool_result is not None:
            return tool_result

        # -----------------------------------------------------
        # REAL AI MODEL
        # -----------------------------------------------------

        ai_response = self.ask_ai(
            command
        )

        if ai_response:
            return ai_response

        # -----------------------------------------------------
        # FALLBACK
        # -----------------------------------------------------

        return self.general_reasoning(
            command
        )

    # =========================================================
    # TOOL DETECTION
    # =========================================================

    def detect_and_use_tool(self, command):

        lowered = command.lower()

        # -----------------------------------------------------
        # CALCULATOR
        # -----------------------------------------------------

        if (
            "calculate" in lowered
            or "what is" in lowered
            or "solve" in lowered
        ):

            expression = self.extract_math_expression(
                command
            )

            if expression:

                return self.execute_tool(
                    "calculator",
                    expression
                )

        # -----------------------------------------------------
        # SYSTEM INFORMATION
        # -----------------------------------------------------

        if (
            "system information" in lowered
            or "system info" in lowered
            or "computer information" in lowered
        ):

            return self.execute_tool(
                "system_info"
            )

        # -----------------------------------------------------
        # LIST FILES
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # WEB SEARCH
        # -----------------------------------------------------

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
                    f"Search prepared for: {query}\n"
                    f"{result}"
                )

        # -----------------------------------------------------
        # CREATE TASK
        # -----------------------------------------------------

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

            return (
                "Tool system is not connected."
            )

        result = self.tools.execute(
            tool_name,
            *args,
            **kwargs
        )

        return result

    # =========================================================
    # TOOL RESULT FORMATTER
    # =========================================================

    def format_tool_result(self, result):

        if isinstance(result, dict):

            lines = []

            for key, value in result.items():

                lines.append(
                    f"{key}: {value}"
                )

            return "\n".join(
                lines
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
    # MATH EXTRACTION
    # =========================================================

    def extract_math_expression(self, command):

        text = command.lower()

        prefixes = [
            "calculate",
            "what is",
            "solve",
            "compute",
        ]

        for prefix in prefixes:

            if text.startswith(prefix):

                expression = command[
                    len(prefix):
                ].strip()

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

    def is_safe_math(self, expression):

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
    # SEARCH QUERY EXTRACTION
    # =========================================================

    def extract_search_query(self, command):

        lowered = command.lower()

        prefixes = [
            "search the web",
            "search online",
            "search",
        ]

        for prefix in prefixes:

            if lowered.startswith(prefix):

                return command[
                    len(prefix):
                ].strip()

        return None

    # =========================================================
    # TASK TITLE EXTRACTION
    # =========================================================

    def extract_task_title(self, command):

        lowered = command.lower()

        prefixes = [
            "create task",
            "add task",
            "make a task",
        ]

        for prefix in prefixes:

            if lowered.startswith(prefix):

                title = command[
                    len(prefix):
                ].strip()

                if title:
                    return title

        return command

    # =========================================================
    # AI PROVIDER
    # =========================================================

    def ask_ai(self, command):

        if not self.model:
            return None

        provider = self.provider.lower().strip()

        if provider == "local":

            return self._ask_local_model(
                command
            )

        return None

    # =========================================================
    # LOCAL MODEL
    # =========================================================

    def _ask_local_model(self, command):

        url = (
            "http://127.0.0.1:11434/api/generate"
        )

        prompt = self._build_prompt(
            command
        )

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature":
                    self.temperature,

                "num_predict":
                    self.max_tokens,
            },
        }

        try:

            request = Request(
                url,
                data=json.dumps(
                    payload
                ).encode("utf-8"),
                headers={
                    "Content-Type":
                        "application/json"
                },
                method="POST",
            )

            with urlopen(
                request,
                timeout=60
            ) as response:

                data = response.read()

            result = json.loads(
                data.decode(
                    "utf-8"
                )
            )

            answer = result.get(
                "response",
                ""
            ).strip()

            if answer:
                return answer

            return None

        except (
            URLError,
            HTTPError,
            TimeoutError,
            OSError,
            json.JSONDecodeError,
        ):

            return None

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

        return (
            f"SYSTEM:\n"
            f"{self.system_role}\n\n"
            f"RECENT CONTEXT:\n"
            f"{history}\n\n"
            f"USER:\n"
            f"{command}\n\n"
            f"EON:"
        )

    # =========================================================
    # STATUS
    # =========================================================

    def system_status(self):

        history_count = len(
            self.context.get_history()
        )

        ai_status = (
            "CONFIGURED"
            if self.model
            else "NOT CONFIGURED"
        )

        tool_status = (
            "CONNECTED"
            if self.tools
            else "NOT CONNECTED"
        )

        return (
            "EON systems are operational.\n"
            f"Brain: {self.status}.\n"
            f"AI Provider: {self.provider}.\n"
            f"AI Model: {self.model or 'None'}.\n"
            f"AI Status: {ai_status}.\n"
            f"Tools: {tool_status}.\n"
            f"Context messages: {history_count}."
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

        history = self.context.get_history()

        if not history:

            return (
                "There is no conversation "
                "history yet."
            )

        return (
            "This session currently contains "
            f"{len(history)} messages."
        )

    # =========================================================
    # FALLBACK
    # =========================================================

    def general_reasoning(self, command):

        return (
            f"I understand your request: "
            f"'{command}'\n"
            "The EON reasoning interface is ready. "
            "Connect a configured AI model to enable "
            "full natural-language reasoning."
        )

    # =========================================================
    # RESET
    # =========================================================

    def reset(self):

        self.context.clear()

        return (
            "EON Brain context has been reset."
        )
