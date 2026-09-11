"""
EON Core
========
Central orchestrator for the Executive Orchestration Network.

EON Core connects:
- Brain
- Router
- Memory
- Tasks
- Agents
- Tools
- Files
- Computer
- Web
- Vision
- Voice
- UI
- Security
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

    def __init__(self):

        # =====================================================
        # CORE
        # =====================================================

        self.context = Context()
        self.brain = Brain(self.context)
        self.router = Router()

        # =====================================================
        # SYSTEM MODULES
        # =====================================================

        self.memory = Memory(
            Config.MEMORY_DATABASE
        )

        self.security = Security(
            require_confirmation=Config.REQUIRE_CONFIRMATION
        )

        self.tasks = TaskEngine()
        self.agents = AgentManager()
        self.tools = ToolRegistry()

        self.files = FileManager()

        self.computer = ComputerController(
            security=self.security
        )

        self.web = WebManager()
        self.vision = Vision()
        self.voice = VoiceManager()
        self.ui = EONUI()

        # =====================================================
        # SYSTEM STATE
        # =====================================================

        self.running = False
        self.mode = Config.MODE

    # =========================================================
    # START EON
    # =========================================================

    def start(self):
        """Start the EON command interface."""

        self.running = True

        self._boot_sequence()

        while self.running:

            try:

                command = input("\nYou: ").strip()

                if not command:
                    continue

                # -------------------------------------------------
                # EXIT COMMAND
                # -------------------------------------------------

                if command.lower() in {
                    "exit",
                    "quit",
                    "shutdown"
                }:
                    self.shutdown()
                    continue

                # -------------------------------------------------
                # MODE CONTROL
                # -------------------------------------------------

                if command.lower() == "kill mode":

                    self.set_mode("KILL")
                    continue

                if command.lower() == "eon has limits":

                    self.set_mode("NORMAL")
                    continue

                # -------------------------------------------------
                # STORE USER MESSAGE
                # -------------------------------------------------

                self.context.add_message(
                    "user",
                    command
                )

                # -------------------------------------------------
                # ROUTE COMMAND
                # -------------------------------------------------

                module = self.router.route(command)

                self.context.set_module(module)

                # -------------------------------------------------
                # PROCESS COMMAND
                # -------------------------------------------------

                response = self.process(
                    command,
                    module
                )

                # -------------------------------------------------
                # STORE RESPONSE
                # -------------------------------------------------

                self.context.add_message(
                    "eon",
                    response
                )

                # -------------------------------------------------
                # DISPLAY RESPONSE
                # -------------------------------------------------

                print()
                print(
                    f"EON [{module.upper()}]:"
                )
                print(response)

            except KeyboardInterrupt:

                self.shutdown()

            except Exception as error:

                print(
                    "\nEON: System error → "
                    f"{error}"
                )

    # =========================================================
    # COMMAND PROCESSOR
    # =========================================================

    def process(self, command, module):
        """Process a command using the appropriate module."""

        command_lower = command.lower().strip()

        # =====================================================
        # BRAIN
        # =====================================================

        if module == "brain":

            self.ui.thinking()

            response = self.brain.think(
                command
            )

            self.ui.idle()

            return response

        # =====================================================
        # MEMORY
        # =====================================================

        if module == "memory":

            return self._process_memory(
                command,
                command_lower
            )

        # =====================================================
        # TASKS
        # =====================================================

        if module == "tasks":

            return self._process_tasks(
                command,
                command_lower
            )

        # =====================================================
        # AGENTS
        # =====================================================

        if module == "agents":

            return self._process_agents(
                command,
                command_lower
            )

        # =====================================================
        # TOOLS
        # =====================================================

        if module == "tools":

            return self._process_tools(
                command,
                command_lower
            )

        # =====================================================
        # FILES
        # =====================================================

        if module == "files":

            return self._process_files(
                command,
                command_lower
            )

        # =====================================================
        # COMPUTER
        # =====================================================

        if module == "computer":

            return self._process_computer(
                command,
                command_lower
            )

        # =====================================================
        # WEB
        # =====================================================

        if module == "web":

            return self._process_web(
                command,
                command_lower
            )

        # =====================================================
        # VISION
        # =====================================================

        if module == "vision":

            return self._process_vision(
                command,
                command_lower
            )

        # =====================================================
        # VOICE
        # =====================================================

        if module == "voice":

            return self._process_voice(
                command,
                command_lower
            )

        # =====================================================
        # FALLBACK
        # =====================================================

        return self.brain.think(command)

    # =========================================================
    # MEMORY PROCESSOR
    # =========================================================

    def _process_memory(self, command, command_lower):

        if (
            "remember" in command_lower
            or "save this" in command_lower
        ):

            content = command

            success = self.memory.remember(
                content
            )

            if success:
                return "Memory saved successfully."

            return "I could not save that memory."

        if (
            "recall" in command_lower
            or "what did i tell you" in command_lower
        ):

            memories = self.memory.recall()

            if not memories:
                return "I don't have any stored memories."

            return self._format_memories(
                memories
            )

        if "clear memory" in command_lower:

            self.memory.clear()

            return "All stored memories have been cleared."

        return (
            "Memory system online.\n"
            f"Stored memories: {self.memory.count()}"
        )

    # =========================================================
    # TASK PROCESSOR
    # =========================================================

    def _process_tasks(self, command, command_lower):

        if "list" in command_lower:

            tasks = self.tasks.list_tasks()

            if not tasks:
                return "There are no tasks."

            lines = []

            for task in tasks:

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

            task_id = self._extract_number(
                command
            )

            if task_id is None:
                return "I could not identify the task number."

            success = self.tasks.complete_task(
                task_id
            )

            if success:
                return (
                    f"Task #{task_id} "
                    "marked as completed."
                )

            return (
                f"Task #{task_id} was not found."
            )

        # Create a new task

        self.context.set_goal(
            command
        )

        task = self.tasks.create_task(
            title=command,
            description="Created by EON."
        )

        self.context.set_task(
            task.task_id
        )

        return (
            f"Goal registered: {command}\n"
            f"Task #{task.task_id} created."
        )

    # =========================================================
    # AGENT PROCESSOR
    # =========================================================

    def _process_agents(self, command, command_lower):

        # -----------------------------------------------------
        # SHOW AGENTS
        # -----------------------------------------------------

        if (
            "list" in command_lower
            or "available" in command_lower
        ):

            agents = self.agents.get_agent_names()

            return (
                "Available EON agents:\n"
                + "\n".join(
                    f"- {agent}"
                    for agent in agents
                )
            )

        # -----------------------------------------------------
        # ASSIGN SIMPLE TASK
        # -----------------------------------------------------

        selected_agent = None

        for agent_id in self.agents.get_agent_names():

            if agent_id in command_lower:

                selected_agent = agent_id
                break

        if selected_agent:

            result = self.agents.assign(
                selected_agent,
                command
            )

            return result

        return (
            "Agent system is online.\n"
            "Available agents: "
            + ", ".join(
                self.agents.get_agent_names()
            )
        )

    # =========================================================
    # TOOL PROCESSOR
    # =========================================================

    def _process_tools(self, command, command_lower):

        if (
            "list" in command_lower
            or "available" in command_lower
        ):

            return (
                "Available EON tools:\n"
                + "\n".join(
                    f"- {tool}"
                    for tool in self.tools.get_tool_names()
                )
            )

        if "calculate" in command_lower:

            return (
                "Calculator tool is registered. "
                "Calculation execution can be connected next."
            )

        return (
            "Tool registry is online.\n"
            f"Available tools: "
            f"{', '.join(self.tools.get_tool_names())}"
        )

    # =========================================================
    # FILE PROCESSOR
    # =========================================================

    def _process_files(self, command, command_lower):

        if "list" in command_lower:

            files = self.files.list_files()

            if not files:
                return "No files found."

            return (
                "Files and folders:\n"
                + "\n".join(
                    f"- {item}"
                    for item in files
                )
            )

        if (
            "read" in command_lower
            and "." in command
        ):

            filename = command.split(
                "read",
                1
            )[-1].strip()

            if not filename:
                return "Please specify a file."

            return self.files.read_file(
                filename
            )

        return (
            "File system module is online.\n"
            "Approved file operations are available."
        )

    # =========================================================
    # COMPUTER PROCESSOR
    # =========================================================

    def _process_computer(
        self,
        command,
        command_lower
    ):

        if "calculator" in command_lower:

            return self.computer.open_application(
                "calculator"
            )

        if "notepad" in command_lower:

            return self.computer.open_application(
                "notepad"
            )

        if "paint" in command_lower:

            return self.computer.open_application(
                "paint"
            )

        if "system info" in command_lower:

            info = self.computer.system_info()

            return self._format_dictionary(
                info
            )

        return (
            "Computer control is online.\n"
            "Approved computer operations are available."
        )

    # =========================================================
    # WEB PROCESSOR
    # =========================================================

    def _process_web(self, command, command_lower):

        if "search" in command_lower:

            query = command

            for word in [
                "search",
                "the web",
                "internet",
                "online"
            ]:

                query = query.replace(
                    word,
                    "",
                ).strip()

            if not query:

                return (
                    "Please specify what "
                    "you want me to search for."
                )

            url = self.web.create_search_url(
                query
            )

            return (
                f"Search prepared for: {query}\n"
                f"Search URL: {url}"
            )

        return "Web intelligence is online."

    # =========================================================
    # VISION PROCESSOR
    # =========================================================

    def _process_vision(
        self,
        command,
        command_lower
    ):

        return (
            "Vision system is online and ready "
            "for visual input."
        )

    # =========================================================
    # VOICE PROCESSOR
    # =========================================================

    def _process_voice(
        self,
        command,
        command_lower
    ):

        if "listen" in command_lower:

            self.ui.listening()

            return self.voice.start_listening()

        if "stop listening" in command_lower:

            return self.voice.stop_listening()

        return (
            "Voice system is online.\n"
            f"Wake word: {self.voice.wake_word}\n"
            "Voice authentication: "
            f"{self.voice.voice_auth_enabled}"
        )

    # =========================================================
    # MEMORY FORMATTER
    # =========================================================

    def _format_memories(self, memories):

        formatted = []

        for memory in memories:

            memory_id = memory[0]
            category = memory[1]
            content = memory[2]

            formatted.append(
                f"[{memory_id}] "
                f"{category}: {content}"
            )

        return "\n".join(
            formatted
        )

    # =========================================================
    # DICTIONARY FORMATTER
    # =========================================================

    def _format_dictionary(self, data):

        lines = []

        for key, value in data.items():

            lines.append(
                f"{key}: {value}"
            )

        return "\n".join(lines)

    # =========================================================
    # NUMBER EXTRACTION
    # =========================================================

    def _extract_number(self, text):

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
    # MODE CONTROL
    # =========================================================

    def set_mode(self, mode):

        mode = mode.upper()

        if mode == "KILL":

            self.mode = "KILL"

            self.ui.set_mode(
                "KILL"
            )

            self.ui.alert()

            print()
            print(
                "EON: LIMITERS... RELEASED."
            )
            print(
                "EON: HIGH-ALERT MODE ACTIVE."
            )

        else:

            self.mode = "NORMAL"

            self.ui.set_mode(
                "NORMAL"
            )

            self.ui.idle()

            print()
            print(
                "EON: NORMAL MODE RESTORED."
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
    # SYSTEM STATUS
    # =========================================================

    def status(self):

        return {
            "name": Config.NAME,
            "version": Config.VERSION,
            "mode": self.mode,
            "running": self.running,

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

    def _status_text(self, status):

        return str(
            status
        ).upper()

    # =========================================================
    # SHUTDOWN
    # =========================================================

    def shutdown(self):

        self.running = False

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
