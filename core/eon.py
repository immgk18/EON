"""
EON Core
=======
Central orchestrator for the Executive Orchestration Network.
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
    """Central EON operating system."""

    def __init__(self):
        # ─────────────────────────────────
        # CORE
        # ─────────────────────────────────

        self.context = Context()
        self.brain = Brain(self.context)
        self.router = Router()

        # ─────────────────────────────────
        # SYSTEM MODULES
        # ─────────────────────────────────

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

        # ─────────────────────────────────
        # SYSTEM STATE
        # ─────────────────────────────────

        self.running = False
        self.mode = Config.MODE

    # ─────────────────────────────────────
    # START
    # ─────────────────────────────────────

    def start(self):
        """Start EON."""

        self.running = True

        self._boot_sequence()

        while self.running:

            try:
                command = input("\nYou: ").strip()

                if not command:
                    continue

                self.context.add_message(
                    "user",
                    command
                )

                # Shutdown
                if command.lower() in {
                    "exit",
                    "quit",
                    "shutdown"
                }:
                    self.shutdown()
                    continue

                # Mode switching
                if command.lower() == "kill mode":
                    self.set_mode("KILL")
                    continue

                if command.lower() == "eon has limits":
                    self.set_mode("NORMAL")
                    continue

                # Route command
                module = self.router.route(command)

                # Process command
                response = self.process(
                    command,
                    module
                )

                # Store response
                self.context.add_message(
                    "eon",
                    response
                )

                print(
                    f"\nEON [{module.upper()}]: "
                    f"{response}"
                )

            except KeyboardInterrupt:
                self.shutdown()

            except Exception as error:
                print(
                    f"\nEON: System error → {error}"
                )

    # ─────────────────────────────────────
    # COMMAND PROCESSING
    # ─────────────────────────────────────

    def process(self, command, module):
        """Process a command using the correct module."""

        command_lower = command.lower()

        # Brain
        if module == "brain":
            self.ui.thinking()

            response = self.brain.think(command)

            self.ui.idle()

            return response

        # Memory
        if module == "memory":

            if "remember" in command_lower:

                content = command

                success = self.memory.remember(
                    content
                )

                if success:
                    return "Memory saved successfully."

                return "I could not save that memory."

            if "recall" in command_lower:

                memories = self.memory.recall()

                if not memories:
                    return "I don't have any stored memories."

                return self._format_memories(
                    memories
                )

            return (
                f"Memory system is online. "
                f"{self.memory.count()} memories stored."
            )

        # Tasks
        if module == "tasks":

            goal = self.tasks.create_goal(
                command
            )

            task = self.tasks.create_task(
                title=command,
                description="Created by EON."
            )

            return (
                f"Goal registered: {goal}\n"
                f"Task #{task.task_id} created."
            )

        # Agents
        if module == "agents":

            names = self.agents.get_agent_names()

            return (
                "Available agents: "
                + ", ".join(names)
            )

        # Files
        if module == "files":

            return (
                "File system module is online. "
                "Specify an approved file operation."
            )

        # Computer
        if module == "computer":

            return (
                "Computer control is online. "
                "Protected actions require authorization."
            )

        # Web
        if module == "web":

            return (
                "Web intelligence module is online."
            )

        # Vision
        if module == "vision":

            return (
                "Vision module is online and "
                "ready for image analysis."
            )

        # Voice
        if module == "voice":

            return (
                "Voice module is online."
            )

        # Tools
        if module == "tools":

            return (
                "Tool registry is online."
            )

        # Default
        return self.brain.think(command)

    # ─────────────────────────────────────
    # MEMORY FORMATTER
    # ─────────────────────────────────────

    def _format_memories(self, memories):
        """Format memories into readable text."""

        formatted = []

        for memory in memories:

            memory_id = memory[0]
            category = memory[1]
            content = memory[2]

            formatted.append(
                f"[{memory_id}] "
                f"{category}: {content}"
            )

        return "\n".join(formatted)

    # ─────────────────────────────────────
    # MODE
    # ─────────────────────────────────────

    def set_mode(self, mode):
        """Change EON operating mode."""

        mode = mode.upper()

        if mode == "KILL":

            self.mode = "KILL"

            self.ui.set_mode("KILL")
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

            self.ui.set_mode("NORMAL")
            self.ui.idle()

            print()
            print(
                "EON: NORMAL MODE RESTORED."
            )
            print(
                "EON HAS LIMITS."
            )

    # ─────────────────────────────────────
    # BOOT
    # ─────────────────────────────────────

    def _boot_sequence(self):
        """Initialize and display EON systems."""

        print()
        print("========================================")
        print("                 E O N")
        print("     EXECUTIVE ORCHESTRATION NETWORK")
        print("========================================")
        print()

        print("EON SYSTEM ONLINE")
        print("----------------------------------------")

        print("CORE       : ONLINE")
        print("BRAIN      : READY")
        print("ROUTER     : READY")
        print("CONTEXT    : READY")

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
            "TASKS      : "
            + self._status_text("READY")
        )

        print(
            "AGENTS     : "
            + self._status_text("READY")
        )

        print(
            "TOOLS      : "
            + self._status_text("READY")
        )

        print(
            "VOICE      : "
            + self._status_text("READY")
        )

        print(
            "VISION     : "
            + self._status_text("READY")
        )

        print(
            "WEB        : "
            + self._status_text("READY")
        )

        print(
            "COMPUTER   : "
            + self._status_text("READY")
        )

        print(
            "FILES      : "
            + self._status_text("READY")
        )

        print("----------------------------------------")
        print(f"MODE       : {self.mode}")
        print("----------------------------------------")
        print()
        print("Awaiting command...")

    def _status_text(self, status):
        """Format a module status."""

        return str(status).upper()

    # ─────────────────────────────────────
    # SHUTDOWN
    # ─────────────────────────────────────

    def shutdown(self):
        """Safely shut down EON."""

        self.running = False

        print()
        print("========================================")
        print("          EON SYSTEM SHUTDOWN")
        print("          SESSION TERMINATED")
        print("========================================")
