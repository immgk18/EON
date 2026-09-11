"""
EON - Executive Orchestration Network
Core Orchestrator

EON Core connects the brain, router, context, and future modules.
"""

from core.brain import Brain
from core.context import Context
from core.router import Router


class EON:
    """Main EON orchestration system."""

    def __init__(self):
        # Core systems
        self.context = Context()
        self.brain = Brain(self.context)
        self.router = Router()

        # System state
        self.running = False
        self.mode = "NORMAL"

    def start(self):
        """Start the EON system."""

        self.running = True

        self._boot_sequence()

        while self.running:
            try:
                command = input("\nYou: ").strip()

                if not command:
                    continue

                # Store user input
                self.context.add_message("user", command)

                # Handle shutdown
                if command.lower() in {
                    "exit",
                    "quit",
                    "shutdown"
                }:
                    self.shutdown()
                    continue

                # Handle mode switching
                if command.lower() == "kill mode":
                    self.set_mode("KILL")
                    continue

                if command.lower() == "eon has limits":
                    self.set_mode("NORMAL")
                    continue

                # Decide which module should handle command
                module = self.router.route(command)

                # Process command
                response = self.process(command, module)

                # Store EON response
                self.context.add_message("eon", response)

                # Display response
                print(f"\nEON [{module.upper()}]: {response}")

            except KeyboardInterrupt:
                self.shutdown()

            except Exception as error:
                print(f"\nEON: Error detected → {error}")

    def process(self, command, module):
        """
        Send the command to the appropriate subsystem.
        """

        if module == "brain":
            return self.brain.think(command)

        return (
            f"{module.capitalize()} module selected. "
            "Module interface is ready for integration."
        )

    def set_mode(self, mode):
        """Change EON operating mode."""

        mode = mode.upper()

        if mode == "KILL":
            self.mode = "KILL"

            print()
            print("EON: LIMITERS... RELEASED.")
            print("EON: HIGH-ALERT MODE ACTIVE.")

        else:
            self.mode = "NORMAL"

            print()
            print("EON: NORMAL MODE RESTORED.")
            print("EON HAS LIMITS.")

    def shutdown(self):
        """Safely shut down EON."""

        self.running = False

        print()
        print("================================")
        print("EON: SYSTEM SHUTDOWN")
        print("EON: SESSION TERMINATED")
        print("================================")

    def _boot_sequence(self):
        """Display the EON startup sequence."""

        print()
        print("========================================")
        print("                 E O N")
        print("     EXECUTIVE ORCHESTRATION NETWORK")
        print("========================================")
        print()
        print("EON SYSTEM ONLINE")
        print("----------------------------")
        print("CORE       : ONLINE")
        print("BRAIN      : READY")
        print("ROUTER     : READY")
        print("CONTEXT    : READY")
        print("MODE       : NORMAL")
        print("----------------------------")
        print()
        print("Awaiting command...")
