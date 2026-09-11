"""
EON Core
========
Executive Orchestration Network.

Central orchestration layer connecting all EON subsystems.
"""

from config import Config

from core.context import Context
from core.router import Router
from core.brain import Brain

from security import Security
from memory import Memory
from tasks import TaskEngine
from agents import AgentManager
from files import FileManager
from web import WebManager
from tools import ToolRegistry
from computer import ComputerController
from vision import Vision
from voice import Voice
from ui import UI
from diagnostics import Diagnostics


class EON:
    """Executive Orchestration Network."""

    def __init__(self):

        # =====================================================
        # CORE STATE
        # =====================================================

        self.running = False
        self.mode = Config.MODE

        # =====================================================
        # CORE
        # =====================================================

        self.context = Context()
        self.router = Router()
        self.security = Security()

        # =====================================================
        # MEMORY
        # =====================================================

        self.memory = Memory(
            database=Config.MEMORY_DATABASE
        )

        # =====================================================
        # TASKS
        # =====================================================

        self.tasks = TaskEngine()

        # =====================================================
        # AGENTS
        # =====================================================

        self.agents = AgentManager()

        # =====================================================
        # FILES
        # =====================================================

        self.files = FileManager()

        # =====================================================
        # WEB
        # =====================================================

        self.web = WebManager()

        # =====================================================
        # TOOLS
        # =====================================================

        self.tools = ToolRegistry(
            file_manager=self.files,
            task_engine=self.tasks,
            web_manager=self.web,
            security=self.security,
        )

        # =====================================================
        # BRAIN
        # =====================================================

        self.brain = Brain(
            self.context,
            tools=self.tools,
            memory=self.memory,
            agents=self.agents,
            tasks=self.tasks,
        )

        # =====================================================
        # COMPUTER
        # =====================================================

        self.computer = ComputerController(
            security=self.security
        )

        # =====================================================
        # VISION
        # =====================================================

        self.vision = Vision()

        # Connect AI provider when supported.
        try:
            self.vision.set_ai_provider(
                self.brain.ai
            )
        except (AttributeError, TypeError):
            pass

        # =====================================================
        # VOICE
        # =====================================================

        self.voice = Voice()

        # =====================================================
        # UI
        # =====================================================

        self.ui = UI()

        # =====================================================
        # DIAGNOSTICS
        # =====================================================

        self.diagnostics = Diagnostics(
            self
        )

    # =========================================================
    # START
    # =========================================================

    def start(self):

        if self.running:
            return

        self.running = True

        self._boot_sequence()

        try:
            self.ui.idle()
        except Exception:
            pass

        print()
        print("EON is ready.")
        print("Type 'help' for commands.")
        print("Type 'health' for diagnostics.")
        print("Type 'shutdown' to stop EON.")
        print()

        while self.running:

            try:

                command = input(
                    "YOU > "
                ).strip()

                if not command:
                    continue

                command_lower = command.lower()

                if command_lower in {
                    "exit",
                    "quit",
                    "shutdown",
                    "stop eon",
                }:
                    self.shutdown()
                    break

                if command_lower in {
                    "kill mode",
                    "activate kill mode",
                    "enter kill mode",
                }:
                    self.set_mode("KILL")
                    continue

                if command_lower in {
                    "eon has limits",
                    "normal mode",
                    "exit kill mode",
                }:
                    self.set_mode("NORMAL")
                    continue

                response = self.handle_command(
                    command
                )

                print()
                print(f"EON > {response}")
                print()

            except KeyboardInterrupt:

                print()
                self.shutdown()

            except Exception as error:

                print()
                print(
                    f"EON ERROR > {error}"
                )
                print()

                self.diagnostics.record_error(
                    "main_loop",
                    error
                )

    # =========================================================
    # COMMAND HANDLER
    # =========================================================

    def handle_command(self, command):

        if not command:
            return "I didn't receive a command."

        self.context.add_message(
            "user",
            command
        )

        # =====================================================
        # DIAGNOSTICS
        # =====================================================

        if command.lower().strip() in {
            "health",
            "health check",
            "diagnostics",
            "run diagnostics",
        }:

            result = (
                self.diagnostics
                .run_health_check()
            )

            response = self._format_result(
                result
            )

            self.context.add_message(
                "assistant",
                response
            )

            return response

        # =====================================================
        # ROUTING
        # =====================================================

        module = self.router.route(
            command
        )

        self.context.set_module(
            module
        )

        # =====================================================
        # PROCESS
        # =====================================================

        try:

            response = self.process(
                command,
                module
            )

        except Exception as error:

            self.diagnostics.record_error(
                module,
                error
            )

            response = (
                "I encountered an internal "
                "error while processing that request."
            )

        self.context.add_message(
            "assistant",
            response
        )

        return response

    # =========================================================
    # PROCESS
    # =========================================================

    def process(self, command, module=None):

        if module is None:
            module = self.router.route(command)

        # Brain handles most intelligent requests.
        if module in {
            "brain",
            "memory",
            "tasks",
            "agents",
            "tools",
            "web",
            "files",
        }:

            return self.brain.think(
                command
            )

        # =====================================================
        # COMPUTER
        # =====================================================

        if module == "computer":

            try:

                result = (
                    self.computer.handle_command(
                        command
                    )
                )

                return self._format_result(
                    result
                )

            except Exception as error:

                self.diagnostics.record_error(
                    "computer",
                    error
                )

                return (
                    "Computer control "
                    "encountered an error."
                )

        # =====================================================
        # VISION
        # =====================================================

        if module == "vision":

            return self._handle_vision(
                command
            )

        # =====================================================
        # VOICE
        # =====================================================

        if module == "voice":

            return self._handle_voice(
                command
            )

        # =====================================================
        # FALLBACK
        # =====================================================

        return self.brain.think(
            command
        )

    # =========================================================
    # VISION
    # =========================================================

    def _handle_vision(self, command):

        image_path = None

        for word in command.split():

            cleaned = word.strip(
                "\"'.,"
            )

            if cleaned.lower().endswith(
                (
                    ".jpg",
                    ".jpeg",
                    ".png",
                    ".webp",
                    ".bmp",
                    ".gif",
                )
            ):

                image_path = cleaned
                break

        if image_path is None:

            return (
                "Please provide an image "
                "path for visual analysis."
            )

        result = self.vision.analyze(
            image_path,
            prompt=command
        )

        if not result.get(
            "success",
            False
        ):

            return result.get(
                "error",
                "Vision analysis failed."
            )

        return result.get(
            "analysis",
            "Vision analysis completed."
        )

    # =========================================================
    # VOICE
    # =========================================================

    def _handle_voice(self, command):

        command_lower = command.lower()

        if "listen" in command_lower:

            result = self.voice.listen()

            if result:
                return result

            return (
                "Voice input is currently "
                "unavailable."
            )

        if "speak" in command_lower:

            message = (
                command
                .split("speak", 1)[1]
                .strip()
                if "speak" in command_lower
                else ""
            )

            if not message:

                return (
                    "Tell me what you "
                    "want me to say."
                )

            success = self.voice.speak(
                message
            )

            if success:

                return (
                    "Voice output completed."
                )

            return (
                "Voice output is currently "
                "unavailable."
            )

        return self.brain.think(
            command
        )

    # =========================================================
    # RESULT FORMATTER
    # =========================================================

    def _format_result(self, result):

        if isinstance(result, str):
            return result

        if result is None:
            return "No result was returned."

        if not isinstance(result, dict):
            return str(result)

        if result.get("success", False):

            if "response" in result:
                return str(
                    result["response"]
                )

            if "analysis" in result:
                return str(
                    result["analysis"]
                )

        if result.get("status") == "HEALTHY":

            return (
                "EON HEALTH: ALL "
                "SYSTEMS OPERATIONAL."
            )

        if result.get("status") == "DEGRADED":

            healthy = result.get(
                "healthy_components",
                0
            )

            total = result.get(
                "total_components",
                0
            )

            return (
                f"EON HEALTH: DEGRADED. "
                f"{healthy}/{total} "
                f"components healthy."
            )

        if "error" in result:
            return str(
                result["error"]
            )

        return str(result)

    # =========================================================
    # MODE
    # =========================================================

    def set_mode(self, mode):

        mode = mode.upper().strip()

        if mode not in {
            "NORMAL",
            "KILL",
        }:
            return False

        self.mode = mode

        if mode == "KILL":

            try:
                self.ui.set_mode("KILL")
                self.ui.alert()
            except Exception:
                pass

            print()
            print(
                "EON > LIMITERS... RELEASED."
            )
            print(
                "EON > HIGH-ALERT MODE ACTIVE."
            )
            print()

        else:

            try:
                self.ui.set_mode("NORMAL")
                self.ui.idle()
            except Exception:
                pass

            print()
            print(
                "EON > EON HAS LIMITS."
            )
            print(
                "EON > NORMAL MODE RESTORED."
            )
            print()

        return True

    # =========================================================
    # BOOT
    # =========================================================

    def _boot_sequence(self):

        print()
        print(
            "===================================="
        )
        print(
            "        EON INITIALIZING"
        )
        print(
            "===================================="
        )

        systems = [
            ("Core systems", True),
            ("Brain", self.brain),
            ("Memory", self.memory),
            ("Task Engine", self.tasks),
            ("Agent System", self.agents),
            ("Tools", self.tools),
            ("Security", self.security),
            ("Vision", self.vision),
            ("Voice", self.voice),
            ("Diagnostics", self.diagnostics),
        ]

        for name, component in systems:

            if component is True:
                status = "ONLINE"
            elif component is not None:
                status = "ONLINE"
            else:
                status = "OFFLINE"

            print(
                f"{name:<19}: {status}"
            )

        print(
            "===================================="
        )

    # =========================================================
    # STATUS
    # =========================================================

    def status(self):

        return {

            "name":
                Config.NAME,

            "full_name":
                Config.FULL_NAME,

            "version":
                Config.VERSION,

            "status":
                "ONLINE"
                if self.running
                else "OFFLINE",

            "mode":
                self.mode,

            "context":
                self.context.status(),

            "router":
                self.router.status(),

            "security":
                self.security.status(),

            "memory":
                self.memory.status(),

            "tasks":
                self.tasks.status(),

            "agents":
                self.agents.status(),

            "tools":
                self.tools.status(),

            "web":
                self.web.status(),

            "computer":
                self.computer.status(),

            "vision":
                self.vision.status(),

            "voice":
                self.voice.status(),

            "ui":
                self.ui.status(),

            "brain":
                self.brain.status(),

            "diagnostics":
                self.diagnostics.status(),
        }

    # =========================================================
    # SHUTDOWN
    # =========================================================

    def shutdown(self):

        if not self.running:
            return

        print()
        print(
            "EON > Shutting down..."
        )

        self.running = False

        try:
            self.voice.stop_speaking()
        except Exception:
            pass

        try:
            self.ui.shutdown()
        except Exception:
            pass

        print(
            "EON > Systems offline."
        )
