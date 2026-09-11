"""
EON Brain
=========
Central reasoning and AI coordination layer for EON.

The Brain:
- Understands user commands
- Maintains conversation context
- Handles basic system commands
- Connects to an external/local AI provider
- Falls back safely when no AI model is available
"""

import json
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from config import Config


class Brain:
    """EON's central reasoning engine."""

    def __init__(self, context):
        self.context = context

        self.name = "EON Brain"
        self.status = "READY"

        self.provider = Config.AI_PROVIDER
        self.model = Config.AI_MODEL
        self.temperature = Config.AI_TEMPERATURE
        self.max_tokens = Config.AI_MAX_TOKENS

        self.system_role = (
            "You are EON, Executive Orchestration Network. "
            "You are a personal AI computing system. "
            "You understand requests, maintain context, "
            "reason about problems, create plans, and coordinate "
            "available EON capabilities. "
            "Be clear, useful, concise, and honest about your abilities."
        )

    # =========================================================
    # MAIN THINKING INTERFACE
    # =========================================================

    def think(self, command):
        """Process a command and generate a response."""

        if not command:
            return "I didn't receive a command."

        command = command.strip()
        lowered = command.lower()

        # Store the command in context
        self.context.add_message(
            "brain",
            command
        )

        # -----------------------------------------------------
        # BASIC SYSTEM COMMANDS
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # BASIC PLANNING
        # -----------------------------------------------------

        if "plan" in lowered or "how do i" in lowered:
            return self.create_basic_plan(command)

        # -----------------------------------------------------
        # REAL AI PROVIDER
        # -----------------------------------------------------

        ai_response = self.ask_ai(command)

        if ai_response:
            return ai_response

        # -----------------------------------------------------
        # SAFE FALLBACK
        # -----------------------------------------------------

        return self.general_reasoning(command)

    # =========================================================
    # AI PROVIDER
    # =========================================================

    def ask_ai(self, command):
        """
        Send the request to the configured AI provider.

        Currently supports the local Ollama HTTP interface.

        If no model is configured or the provider is unavailable,
        EON safely falls back to its built-in reasoning interface.
        """

        if not self.model:
            return None

        provider = self.provider.lower().strip()

        if provider == "local":
            return self._ask_local_model(command)

        return None

    def _ask_local_model(self, command):
        """Send a request to a local Ollama model."""

        url = "http://127.0.0.1:11434/api/generate"

        prompt = self._build_prompt(command)

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
        }

        try:
            request = Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Content-Type": "application/json"
                },
                method="POST",
            )

            with urlopen(
                request,
                timeout=60
            ) as response:

                data = response.read()

            result = json.loads(
                data.decode("utf-8")
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
        """Build the prompt sent to the AI model."""

        recent_history = self.context.get_recent(8)

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

        history = "\n".join(history_text)

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
    # SYSTEM STATUS
    # =========================================================

    def system_status(self):
        """Return the current Brain status."""

        history_count = len(
            self.context.get_history()
        )

        ai_status = (
            "CONFIGURED"
            if self.model
            else "NOT CONFIGURED"
        )

        return (
            "EON systems are operational.\n"
            f"Brain: {self.status}.\n"
            f"AI Provider: {self.provider}.\n"
            f"AI Model: {self.model or 'None'}.\n"
            f"AI Status: {ai_status}.\n"
            f"Context messages: {history_count}."
        )

    # =========================================================
    # HELP
    # =========================================================

    def help(self):
        """Return EON capability information."""

        return (
            "I can understand requests, maintain context, "
            "plan tasks, route commands, work with files, "
            "use tools, coordinate agents, process visual input, "
            "use web information, manage memory, and interact "
            "through voice."
        )

    # =========================================================
    # TIME
    # =========================================================

    def current_time(self):
        """Return the current local time."""

        now = datetime.now()

        return (
            "The current local time is "
            f"{now.strftime('%I:%M:%S %p')}."
        )

    # =========================================================
    # HISTORY
    # =========================================================

    def history_summary(self):
        """Return a summary of the current session."""

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
    # BASIC PLANNER
    # =========================================================

    def create_basic_plan(self, command):
        """Create a basic execution plan."""

        return (
            "I would approach this in these stages:\n"
            "1. Understand the objective.\n"
            "2. Break it into smaller tasks.\n"
            "3. Select the appropriate EON capabilities.\n"
            "4. Execute the approved steps.\n"
            "5. Verify the results.\n"
            "6. Report the outcome."
        )

    # =========================================================
    # FALLBACK REASONING
    # =========================================================

    def general_reasoning(self, command):
        """Fallback when no AI provider is available."""

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
        """Reset the Brain session context."""

        self.context.clear()

        return (
            "EON Brain context has been reset."
        )
