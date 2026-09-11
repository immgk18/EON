"""
EON Core
========
Central orchestration layer for EON.

EON coordinates:
- Brain
- Context
- Router
- Security
- Memory
- Tasks
- Agents
- Tools
- Files
- Web
- Computer
- Vision
- Voice
- UI
- Diagnostics
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
        # CORE SYSTEMS
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
        # TASK ENGINE
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
        # COMPUTER CONTROL
        # =====================================================

        self.computer = ComputerControl(
            security=self.security
        )

        # =====================================================
        # VISION
        # =====================================================

        self.vision = Vision(
            ai_provider=self.brain.ai
        )

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

        self.ui.idle()

        print()
        print("EON is ready.")
        print("Type 'help' for commands.")
        print("Type 'shutdown' to stop EON.")
        print()

        while self.running:

            try:

                command = input("YOU > ").strip()

                if not command:
                    continue

                command_lower = command.lower()

                # -------------------------------------------------
                # Shutdown
                # -------------------------------------------------

                if command_lower in {
                    "exit",
                    "quit",
                    "shutdown",
                    "stop eon",
                }:

                    self.shutdown()
                    break

                # -------------------------------------------------
                # Kill Mode
                # -------------------------------------------------

                if command_lower in {
                    "kill mode",
                    "activate kill mode",
                    "enter kill mode",
                }:

                    self.set_mode("KILL")
                    continue

                # -------------------------------------------------
                # Normal Mode
                # -------------------------------------------------

                if command_lower in {
                    "eon has limits",
                    "normal mode",
                    "exit kill mode",
                }:

                    self.set_mode("NORMAL")
                    continue

                # -------------------------------------------------
                # Process command
                # -------------------------------------------------

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

                if self.diagnostics:
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

        # -----------------------------------------------------
        # Store user command
        # -----------------------------------------------------

        self.context.add_message(
            "user",
            command
        )

        # -----------------------------------------------------
        # Diagnostics command
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # Route
        # -----------------------------------------------------

        module = self.router.route(
            command
        )

        self.context.set_module(
            module
        )

        # -----------------------------------------------------
        # Process
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # Store response
        # -----------------------------------------------------

        self.context.add_message(
            "assistant",
            response
        )

        return response

    # =========================================================
    # PROCESS
    # =========================================================

    def process(
        self,
        command,
        module=None
    ):

        if module is None:

            module = self.router.route(
                command
            )

        # -----------------------------------------------------
        # Brain
        # -----------------------------------------------------

        if module == "brain":

            return self.brain.think(
                command
            )

        # -----------------------------------------------------
        # Memory
        # -----------------------------------------------------

        if module == "memory":

            return self.brain.think(
                command
            )

        # -----------------------------------------------------
        # Tasks
        # -----------------------------------------------------

        if module == "tasks":

            return self.brain.think(
                command
            )

        # -----------------------------------------------------
        # Agents
        # -----------------------------------------------------

        if module == "agents":

            return self.brain.think(
                command
            )

        # -----------------------------------------------------
        # Tools
        # -----------------------------------------------------

        if module == "tools":

            return self.brain.think(
                command
            )

        # -----------------------------------------------------
        # Web
        # -----------------------------------------------------

        if module == "web":

            return self.brain.think(
                command
            )

        # -----------------------------------------------------
        # Files
        # -----------------------------------------------------

        if module == "files":

            return self.brain.think(
                command
            )

        # -----------------------------------------------------
        # Computer
        # -----------------------------------------------------

        if module == "computer":

            result = self.computer.handle_command(
                command
            )

            return self._format_result(
                result
            )

        # -----------------------------------------------------
        # Vision
        # -----------------------------------------------------

        if module == "vision":

            return self._handle_vision(
                command
            )

        # -----------------------------------------------------
        # Voice
        # -----------------------------------------------------

        if module == "voice":

            return self._handle_voice(
                command
            )

        # -----------------------------------------------------
        # Default
        # -----------------------------------------------------

        return self.brain.think(
            command
        )

    # =========================================================
    # VISION
    # =========================================================

    def _handle_vision(
        self,
        command
    ):

        words = command.split()

        image_path = None

        for word in words:

            if word.lower().endswith(
                (
                    ".jpg",
                    ".jpeg",
                    ".png",
                    ".webp",
                    ".bmp",
                    ".gif",
                )
            ):

                image_path = word.strip(
                    "\"'"
                )

                break

        if image_path is None:

            return (
                "Please provide an image path "
                "for visual analysis."
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

    def _handle_voice(
        self,
        command
    ):

        command_lower = (
            command.lower()
        )

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
                .lower()
                .replace("speak", "", 1)
                .strip()
            )

            if not message:

                return (
                    "Tell me what you want "
                    "me to say."
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

    def _format_result(
        self,
        result
    ):

        if isinstance(
            result,
            str
        ):

            return result

        if not isinstance(
            result,
            dict
        ):

            return str(result)

        if result.get(
            "success",
            False
        ):

            if "response" in result:
                return str(
                    result["response"]
                )

            if "analysis" in result:
                return str(
                    result["analysis"]
                )

            if result.get(
                "status"
            ) == "HEALTHY":

                return (
                    "EON HEALTH: ALL "
                    "SYSTEMS OPERATIONAL."
                )

            return str(result)

        return result.get(
            "error",
            str(result)
        )

    # =========================================================
    # MODE
    # =========================================================

    def set_mode(
        self,
        mode
    ):

        mode = mode.upper()

        if mode not in {
            "NORMAL",
            "KILL",
        }:

            return False

        self.mode = mode

        if mode == "KILL":

            self.ui.set_mode(
                "KILL"
            )

            self.ui.alert()

            print()
            print(
                "EON > LIMITERS... RELEASED."
            )
            print(
                "EON > HIGH-ALERT MODE ACTIVE."
            )
            print()

        else:

            self.ui.set_mode(
                "NORMAL"
            )

            self.ui.idle()

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

        print(
            "Core systems      : ONLINE"
        )

        print(
            "Brain             : ONLINE"
        )

        print(
            "Memory            : ONLINE"
        )

        print(
            "Task Engine       : ONLINE"
        )

        print(
            "Agent System      : ONLINE"
        )

        print(
            "Tools             : ONLINE"
        )

        print(
            "Security          : ONLINE"
        )

        print(
            "Vision            : ONLINE"
        )

        print(
            "Voice             : ONLINE"
        )

        print(
            "Diagnostics       : ONLINE"
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
