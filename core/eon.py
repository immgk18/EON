from core.brain import Brain
from core.context import Context
from core.router import Router


class EON:
    """Executive Orchestration Network."""

    def __init__(self):
        self.context = Context()
        self.brain = Brain(self.context)
        self.router = Router()

        self.running = False
        self.mode = "NORMAL"

    def start(self):
        self.running = True

        self.display_boot()

        while self.running:
            try:
                command = input("\nYou: ").strip()

                if not command:
                    continue

                self.context.add_message("user", command)

                if command.lower() in ["exit", "quit", "shutdown"]:
                    self.shutdown()
                    continue

                if command.lower() == "kill mode":
                    self.set_mode("KILL")
                    continue

                if command.lower() == "eon has limits":
                    self.set_mode("NORMAL")
                    continue

                module = self.router.route(command)

                response = self.process(command, module)

                self.context.add_message("eon", response)

                print(f"EON [{module.upper()}]: {response}")

            except KeyboardInterrupt:
                self.shutdown()

    def process(self, command, module):
        """Process a command through the appropriate subsystem."""

        if module == "brain":
            return self.brain.think(command)

        return (
            f"Command routed to the {module} module. "
            f"The module interface is ready for implementation."
        )

    def set_mode(self, mode):
        self.mode = mode

        if mode == "KILL":
            print("\nEON: LIMITERS... RELEASED.")
            print("EON HIGH-ALERT MODE ACTIVE.")

        else:
            print("\nEON: NORMAL MODE RESTORED.")
            print("EON HAS LIMITS.")

    def display_boot(self):
        print()
        print("========================================")
        print("                 E O N")
        print("       EXECUTIVE ORCHESTRATION")
        print("              NETWORK")
        print("========================================")
        print()
        print("EON SYSTEM ONLINE")
        print("CORE STATUS   : ONLINE")
        print("BRAIN         : READY")
        print("ROUTER        : READY")
        print("CONTEXT       : READY")
        print("MODE          : NORMAL")
        print()
        print("Awaiting command...")

    def shutdown(self):
        self.running = False

        print()
        print("EON: Shutting down.")
        print("EON: Session terminated.")
