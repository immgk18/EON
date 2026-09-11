"""
EON Core
========
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
    """Central EON orchestration system."""

    def __init__(self):

        # ─────────────────────────────────
        # CORE
        # ─────────────────────────────────

        self.context = Context()
        self.brain = Brain(self.context)
        self.router = Router()

        # ─────────────────────────────────
        # MODULES
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
        # STATE
        # ─────────────────────────────────

        self.running = False
        self.mode = Config.MODE

    # ─────────────────────────────────────
    # START
    # ─────────────────────────────────────

    def start(self):
        """Start the EON system."""

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

                self.context.set_module(module)

                # Process command
                response = self.process(
                    command,
                    module
                )

                # Save response
                self.context.add_message(
                    "eon",
                    response
                )

                print()
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

    # ─────────────────────────────────────
    # PROCESS
    # ─────────────────────────────────────

    def process(self, command, module):
        """Process a command through the selected module."""

        command_lower = command.lower()

        # ─────────────────────────────────
        # BRAIN
        # ─────────────────────────────────

        if module == "brain":

            self.ui.thinking()

            response = self.brain.think(
                command
            )

            self.ui.idle()

            return response

        # ─────────────────────────────────
        # MEMORY
        # ─────────────────────────────────

        if module == "memory":

            if "remember" in command_lower:

                success = self.memory.remember(
                    command
                )

                if success:
                    return "Memory saved successfully."

                return "I could not save that memory."

            if "recall" in command_lower:

                memories = self.memory.recall()

                if not memories:
                    return (
                        "I don't have any stored memories."
                    )

                return self._format_memories(
                    memories
                )

            return (
                f"Memory system online. "
                f"{self.memory.count()} memories stored."
            )

        # ─────────────────────────────────
        # TASKS
        # ─────────────────────────────────

        if module == "tasks":

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

        # ─────────────────────────────────
        # AGENTS
        # ─────────────────────────────────

        if module == "agents":

            agents = self.agents.get_agent_names()

            return (
                "Available EON agents:\n"
                + "\n".join(
                    f"- {agent}"
                    for agent in agents
                )
            )

        # ─────────────────────────────────
        # FILES
        # ─────────────────────────────────

        if module == "files":

            return (
                "File system module is online. "
                "Approved file operations are available."
            )

        # ─────────────────────────────────
        # COMPUTER
        # ─────────────────────────────────

        if module == "computer":

            return (
                "Computer control is online. "
                "Protected operations require authorization."
            )

        # ─────────────────────────────────
        # WEB
        # ─────────────────────────────────

        if module == "web":

            return (
                "Web intelligence is online."
            )

        # ─────────────────────────────────
        # VISION
        # ─────────────────────────────────

        if module == "vision":

            return (
                "Vision system is online and "
                "ready for visual input."
            )

        # ─────────────────────────────────
        # VOICE
        # ─────────────────────────────────

        if module == "voice":

            return (
                "Voice system is online."
            )

        # ─────────────────────────────────
        # TOOLS
        # ─────────────────────────────────

        if module == "tools":

            return (
                "Tool registry is online.\n"
                f"Available tools: "
                f"{', '.join(self.tools.get_tool_names())}"
            )

        # ─────────────────────────────────
        # FALLBACK
        # ─────────────────────────────────

        return self.brain.think(
            command
        )

    # ─────────────────────────────────────
    # MEMORY FORMAT
    # ─────────────────────────────────────

    def _format_memories(self, memories):
        """Format stored memories."""

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
        """Display EON startup information."""

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

        print("TASKS      : READY")
        print("AGENTS     : READY")
        print("TOOLS      : READY")
        print("FILES      : READY")
        print("COMPUTER   : READY")
        print("WEB        : READY")
        print("VISION     : READY")
        print("VOICE      : READY")

        print("----------------------------------------")
        print(f"MODE       : {self.mode}")
        print("----------------------------------------")

        print()
        print("Awaiting command...")

    # ─────────────────────────────────────
    # STATUS
    # ─────────────────────────────────────

    def status(self):
        """Return a complete EON status snapshot."""

        return {
            "name": Config.NAME,
            "version": Config.VERSION,
            "mode": self.mode,
            "running": self.running,
            "context": self.context.status(),
            "memory": self.memory.status(),
            "security": self.security.status(),
            "tasks": self.tasks.status(),
            "agents": self.agents.status(),
            "tools": self.tools.status(),
            "computer": self.computer.status(),
            "web": self.web.status(),
            "vision": self.vision.status(),
            "voice": self.voice.status(),
            "ui": self.ui.status(),
        }

    # ─────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────

    def _status_text(self, status):
        """Format a status value."""

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
