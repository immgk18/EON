"""
EON Core
========
Central orchestration system for EON.

Pipeline:

INPUT
  ↓
ROUTER
  ↓
BRAIN / MODULE
  ↓
TOOLS / AGENTS / TASKS
  ↓
MEMORY / CONTEXT
  ↓
VOICE / UI
  ↓
OUTPUT
"""

from core.brain import Brain
from core.context import Context
from core.router import Router

from agents import AgentManager
from memory import Memory
from security import Security
from tasks import TaskEngine
from tools import ToolRegistry
from files import FileManager
from computer import ComputerController
from web import WebManager
from vision import Vision
from voice import VoiceManager
from ui import EONUI

from config import Config


class EON:
    """Main EON orchestration system."""

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(self):

        # -----------------------------------------------------
        # Core
        # -----------------------------------------------------

        self.context = Context()
        self.router = Router()

        # -----------------------------------------------------
        # Security
        # -----------------------------------------------------

        self.security = Security(
            require_confirmation=Config.REQUIRE_CONFIRMATION
        )

        # -----------------------------------------------------
        # Memory
        # -----------------------------------------------------

        self.memory = Memory(
            Config.MEMORY_DATABASE
        )

        # -----------------------------------------------------
        # Task Engine
        # -----------------------------------------------------

        self.tasks = TaskEngine()

        # -----------------------------------------------------
        # Agents
        # -----------------------------------------------------

        self.agents = AgentManager()

        # -----------------------------------------------------
        # Files
        # -----------------------------------------------------

        self.files = FileManager()

        # -----------------------------------------------------
        # Web
        # -----------------------------------------------------

        self.web = WebManager()

        # -----------------------------------------------------
        # Tools
        # -----------------------------------------------------

        self.tools = ToolRegistry(
            file_manager=self.files,
            task_engine=self.tasks,
            web_manager=self.web,
            security=self.security,
        )

        # -----------------------------------------------------
        # Brain
        # -----------------------------------------------------

        self.brain = Brain(
            self.context,
            tools=self.tools,
            memory=self.memory,
            agents=self.agents,
            tasks=self.tasks,
        )

        # -----------------------------------------------------
        # Computer
        # -----------------------------------------------------

        self.computer = ComputerController(
            security=self.security
        )

        # -----------------------------------------------------
        # Vision
        # -----------------------------------------------------

        self.vision = Vision()

        # -----------------------------------------------------
        # Voice
        # -----------------------------------------------------

        self.voice = VoiceManager(
            wake_word=Config.WAKE_WORD,
            language=Config.VOICE_LANGUAGE,
        )

        # -----------------------------------------------------
        # UI
        # -----------------------------------------------------

        self.ui = EONUI()

        # -----------------------------------------------------
        # System State
        # -----------------------------------------------------

        self.running = False
        self.mode = Config.MODE

    # =========================================================
    # START
    # =========================================================

    def start(self):

        self.running = True

        self._boot_sequence()

        self.ui.idle()

        while self.running:

            try:

                command = input(
                    "\nYou: "
                ).strip()

                if not command:
                    continue

                # -------------------------------------------------
                # Shutdown
                # -------------------------------------------------

                if command.lower() in {
                    "exit",
                    "quit",
                    "shutdown",
                }:

                    self.shutdown()
                    continue

                # -------------------------------------------------
                # High-alert mode
                # -------------------------------------------------

                if command.lower() == "kill mode":

                    self.set_mode("KILL")
                    continue

                # -------------------------------------------------
                # Normal mode
                # -------------------------------------------------

                if command.lower() == "eon has limits":

                    self.set_mode("NORMAL")
                    continue

                # -------------------------------------------------
                # Central command handler
                # -------------------------------------------------

                response = self.handle_command(
                    command
                )

                print()

                module = (
                    self.context.get_module()
                    or "brain"
                )

                print(
                    f"EON [{module.upper()}]:"
                )

                print(response)

            except KeyboardInterrupt:

                self.shutdown()

            except Exception as error:

                print(
                    f"\nEON: System error → {error}"
                )

    # =========================================================
    # CENTRAL COMMAND HANDLER
    # =========================================================

    def handle_command(
        self,
        command
    ):

        if not command:

            return (
                "I didn't receive a command."
            )

        # -----------------------------------------------------
        # Save user command
        # -----------------------------------------------------

        self.context.add_message(
            "user",
            command
        )

        # -----------------------------------------------------
        # Route command
        # -----------------------------------------------------

        module = self.router.route(
            command
        )

        self.context.set_module(
            module
        )

        # -----------------------------------------------------
        # Process command
        # -----------------------------------------------------

        response = self.process(
            command,
            module
        )

        # -----------------------------------------------------
        # Save EON response
        # -----------------------------------------------------

        self.context.add_message(
            "eon",
            response
        )

        return response

    # =========================================================
    # PROCESS
    # =========================================================

    def process(
        self,
        command,
        module
    ):

        command_lower = (
            command.lower().strip()
        )

        # -----------------------------------------------------
        # Brain
        # -----------------------------------------------------

        if module == "brain":

            self.ui.thinking()

            response = self.brain.think(
                command
            )

            self.ui.speaking()

            return response

        # -----------------------------------------------------
        # Memory
        # -----------------------------------------------------

        if module == "memory":

            return self._process_memory(
                command,
                command_lower
            )

        # -----------------------------------------------------
        # Tasks
        # -----------------------------------------------------

        if module == "tasks":

            return self._process_tasks(
                command,
                command_lower
            )

        # -----------------------------------------------------
        # Agents
        # -----------------------------------------------------

        if module == "agents":

            return self._process_agents(
                command,
                command_lower
            )

        # -----------------------------------------------------
        # Tools
        # -----------------------------------------------------

        if module == "tools":

            return self._process_tools(
                command,
                command_lower
            )

        # -----------------------------------------------------
        # Files
        # -----------------------------------------------------

        if module == "files":

            return self._process_files(
                command,
                command_lower
            )

        # -----------------------------------------------------
        # Computer
        # -----------------------------------------------------

        if module == "computer":

            return self._process_computer(
                command,
                command_lower
            )

        # -----------------------------------------------------
        # Web
        # -----------------------------------------------------

        if module == "web":

            return self._process_web(
                command,
                command_lower
            )

        # -----------------------------------------------------
        # Vision
        # -----------------------------------------------------

        if module == "vision":

            return self._process_vision(
                command,
                command_lower
            )

        # -----------------------------------------------------
        # Voice
        # -----------------------------------------------------

        if module == "voice":

            return self._process_voice(
                command,
                command_lower
            )

        # -----------------------------------------------------
        # Fallback
        # -----------------------------------------------------

        self.ui.thinking()

        return self.brain.think(
            command
        )

    # =========================================================
    # MEMORY
    # =========================================================

    def _process_memory(
        self,
        command,
        command_lower
    ):

        if (
            "remember" in command_lower
            or "save this" in command_lower
        ):

            success = self.memory.remember(
                command
            )

            if success:

                return (
                    "Memory saved successfully."
                )

            return (
                "I could not save that memory."
            )

        if (
            "recall" in command_lower
            or "what did i tell you"
            in command_lower
        ):

            memories = (
                self.memory.recall()
            )

            if not memories:

                return (
                    "I don't have any stored memories."
                )

            return self._format_memories(
                memories
            )

        if "clear memory" in command_lower:

            self.memory.clear()

            return (
                "All stored memories have been cleared."
            )

        return (
            "Memory system online.\n"
            f"Stored memories: "
            f"{self.memory.count()}"
        )

    # =========================================================
    # TASKS
    # =========================================================

    def _process_tasks(
        self,
        command,
        command_lower
    ):

        if "list" in command_lower:

            task_list = (
                self.tasks.list_tasks()
            )

            if not task_list:

                return (
                    "There are no tasks."
                )

            lines = []

            for task in task_list:

                lines.append(
                    f"#{task.task_id} | "
                    f"{task.title} | "
                    f"{task.status}"
                )

            return "\n".join(lines)

        if (
            "complete" in command_lower
            and any(
                character.isdigit()
                for character in command
            )
        ):

            task_id = (
                self._extract_number(
                    command
                )
            )

            if task_id is None:

                return (
                    "I could not identify "
                    "the task number."
                )

            success = (
                self.tasks.complete_task(
                    task_id
                )
            )

            if success:

                return (
                    f"Task #{task_id} "
                    "marked as completed."
                )

            return (
                f"Task #{task_id} "
                "was not found."
            )

        # -----------------------------------------------------
        # Create new task
        # -----------------------------------------------------

        self.context.set_goal(
            command
        )

        task = self.tasks.create_task(
            title=command,
            description="Created by EON.",
        )

        self.context.set_task(
            task.task_id
        )

        return (
            f"Goal registered: {command}\n"
            f"Task #{task.task_id} created."
        )

    # =========================================================
    # AGENTS
    # =========================================================

    def _process_agents(
        self,
        command,
        command_lower
    ):

        if (
            "list" in command_lower
            or "available" in command_lower
        ):

            agents = (
                self.agents.get_agent_names()
            )

            return (
                "Available EON agents:\n"
                + "\n".join(
                    f"- {agent}"
                    for agent in agents
                )
            )

        selected_agent = (
            self.agents.select_agent(
                command
            )
        )

        if selected_agent:

            return self.agents.assign(
                selected_agent,
                command
            )

        return (
            "Agent system is online.\n"
            "Available agents: "
            + ", ".join(
                self.agents.get_agent_names()
            )
        )

    # =========================================================
    # TOOLS
    # =========================================================

    def _process_tools(
        self,
        command,
        command_lower
    ):

        if (
            "list" in command_lower
            or "available" in command_lower
        ):

            return (
                "Available EON tools:\n"
                + "\n".join(
                    f"- {tool}"
                    for tool
                    in self.tools.get_tool_names()
                )
            )

        if "calculate" in command_lower:

            expression = (
                command_lower
                .replace(
                    "calculate",
                    "",
                    1
                )
                .strip()
            )

            return self.tools.execute(
                "calculator",
                expression
            )

        return (
            "Tool registry is online.\n"
            f"Available tools: "
            f"{', '.join(self.tools.get_tool_names())}"
        )

    # =========================================================
    # FILES
    # =========================================================

    def _process_files(
        self,
        command,
        command_lower
    ):

        if (
            "list" in command_lower
            or "show files" in command_lower
        ):

            files = (
                self.files.list_files()
            )

            if not files:

                return "No files found."

            return (
                "Files and folders:\n"
                + "\n".join(
                    f"- {item}"
                    for item in files
                )
            )

        if "read" in command_lower:

            filename = (
                command_lower
                .split(
                    "read",
                    1
                )[-1]
                .strip()
            )

            if not filename:

                return (
                    "Please specify a file."
                )

            return self.files.read_file(
                filename
            )

        return (
            "File system module is online.\n"
            "Approved file operations are available."
        )

    # =========================================================
    # COMPUTER
    # =========================================================

    def _process_computer(
        self,
        command,
        command_lower
    ):

        if "calculator" in command_lower:

            result = (
                self.computer.open_application(
                    "calculator"
                )
            )

            return self._format_result(
                result
            )

        if "notepad" in command_lower:

            result = (
                self.computer.open_application(
                    "notepad"
                )
            )

            return self._format_result(
                result
            )

        if "paint" in command_lower:

            result = (
                self.computer.open_application(
                    "paint"
                )
            )

            return self._format_result(
                result
            )

        if (
            "system info" in command_lower
            or "system information"
            in command_lower
        ):

            return self._format_result(
                self.computer.system_info()
            )

        return (
            "Computer control is online.\n"
            "Approved computer operations are available."
        )

    # =========================================================
    # WEB
    # =========================================================

    def _process_web(
        self,
        command,
        command_lower
    ):

        if (
            "search" in command_lower
            or "look up" in command_lower
        ):

            query = command

            prefixes = [
                "search",
                "look up",
                "search the web",
            ]

            for prefix in prefixes:

                if query.lower().startswith(
                    prefix
                ):

                    query = (
                        query[
                            len(prefix):
                        ].strip()
                    )

                    break

            if not query:

                return (
                    "Please specify what "
                    "you want me to search for."
                )

            return self.tools.execute(
                "web_search",
                query
            )

        return (
            "Web intelligence is online."
        )

    # =========================================================
    # VISION
    # =========================================================

    def _process_vision(
        self,
        command,
        command_lower
    ):

        return (
            "Vision system is online "
            "and ready for visual input."
        )

    # =========================================================
    # VOICE
    # =========================================================

    def _process_voice(
        self,
        command,
        command_lower
    ):

        if "listen" in command_lower:

            self.ui.listening()

            result = (
                self.voice.start_listening()
            )

            return self._format_result(
                result
            )

        if "stop listening" in command_lower:

            result = (
                self.voice.stop_listening()
            )

            return self._format_result(
                result
            )

        return (
            "Voice system is online.\n"
            f"Wake word: "
            f"{self.voice.wake_word}\n"
            "Voice authentication: "
            f"{self.voice.voice_auth_enabled}"
        )

    # =========================================================
    # FORMAT RESULT
    # =========================================================

    def _format_result(
        self,
        result
    ):

        if isinstance(
            result,
            dict
        ):

            return "\n".join(
                f"{key}: {value}"
                for key, value
                in result.items()
            )

        if isinstance(
            result,
            list
        ):

            if not result:

                return "No results found."

            return "\n".join(
                f"- {item}"
                for item in result
            )

        return str(result)

    # =========================================================
    # FORMAT MEMORIES
    # =========================================================

    def _format_memories(
        self,
        memories
    ):

        formatted = []

        for memory in memories:

            memory_id = memory[0]
            category = memory[1]
            content = memory[2]

            formatted.append(
                f"[{memory_id}] "
                f"{category}: "
                f"{content}"
            )

        return "\n".join(
            formatted
        )

    # =========================================================
    # NUMBER EXTRACTION
    # =========================================================

    def _extract_number(
        self,
        text
    ):

        current_number = ""

        for character in text:

            if character.isdigit():

                current_number += character

            elif current_number:

                break

        if current_number:

            return int(
                current_number
            )

        return None

    # =========================================================
    # MODE
    # =========================================================

    def set_mode(
        self,
        mode
    ):

        mode = mode.upper()

        if mode == "KILL":

            self.mode = "KILL"

            self.ui.set_mode(
                "KILL"
            )

            self.ui.alert()

            print(
                "\nEON: "
                "LIMITERS... RELEASED."
            )

            print(
                "EON: "
                "HIGH-ALERT MODE ACTIVE."
            )

        else:

            self.mode = "NORMAL"

            self.ui.set_mode(
                "NORMAL"
            )

            self.ui.idle()

            print(
                "\nEON: "
                "NORMAL MODE RESTORED."
            )

            print(
                "EON HAS LIMITS."
            )

    # =========================================================
    # BOOT SEQUENCE
    # =========================================================

    def _boot_sequence(self):

        print()

        print(
            "========================================"
        )

        print(
            "                 E O N"
        )

        print(
            "     EXECUTIVE ORCHESTRATION NETWORK"
        )

        print(
            "========================================"
        )

        print()

        print(
            "EON SYSTEM ONLINE"
        )

        print(
            "----------------------------------------"
        )

        print(
            "CORE       : ONLINE"
        )

        print(
            "BRAIN      : READY"
        )

        print(
            "ROUTER     : READY"
        )

        print(
            "CONTEXT    : READY"
        )

        print(
            "MEMORY     : "
            + self._status_text(
                self.memory.status()["status"]
            )
        )

        print(
            "SECURITY   : "
            + self._status_text(
                "ONLINE"
                if self.security.enabled
                else "OFFLINE"
            )
        )

        print(
            "TASKS      : READY"
        )

        print(
            "AGENTS     : READY"
        )

        print(
            "TOOLS      : READY"
        )

        print(
            "FILES      : READY"
        )

        print(
            "COMPUTER   : READY"
        )

        print(
            "WEB        : READY"
        )

        print(
            "VISION     : READY"
        )

        print(
            "VOICE      : READY"
        )

        print(
            "UI         : READY"
        )

        print(
            "----------------------------------------"
        )

        print(
            f"MODE       : {self.mode}"
        )

        print(
            "----------------------------------------"
        )

        print()

        print(
            "Awaiting command..."
        )

    # =========================================================
    # STATUS
    # =========================================================

    def status(self):

        return {

            "name":
                Config.NAME,

            "version":
                Config.VERSION,

            "mode":
                self.mode,

            "running":
                self.running,

            "context":
                self.context.status(),

            "memory":
                self.memory.status(),

            "security":
                self.security.status(),

            "tasks":
                self.tasks.status(),

            "agents":
                self.agents.status(),

            "tools":
                self.tools.status(),

            "computer":
                self.computer.status(),

            "web":
                self.web.status(),

            "vision":
                self.vision.status(),

            "voice":
                self.voice.status(),

            "ui":
                self.ui.status(),
        }

    # =========================================================
    # STATUS TEXT
    # =========================================================

    def _status_text(
        self,
        status
    ):

        return str(
            status
        ).upper()

    # =========================================================
    # SHUTDOWN
    # =========================================================

    def shutdown(self):

        self.running = False

        self.voice.stop_listening()

        self.ui.shutdown()

        print()

        print(
            "========================================"
        )

        print(
            "          EON SYSTEM SHUTDOWN"
        )

        print(
            "          SESSION TERMINATED"
        )

        print(
            "========================================"
        )
