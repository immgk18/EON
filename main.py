import os
import platform
from datetime import datetime


# ============================================================
#                         EON v0.1
#              Executive Orchestration Network
# ============================================================

EON_NAME = "EON"
VERSION = "0.1"


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def get_system_status():
    """Return basic information about the computer."""
    return {
        "System": platform.system(),
        "Release": platform.release(),
        "Machine": platform.machine(),
        "Processor": platform.processor() or "Unknown",
        "Python": platform.python_version()
    }


def show_status():
    """Display EON system status."""
    status = get_system_status()

    print("\n" + "=" * 50)
    print("                 E O N")
    print("=" * 50)

    print("\nSTATUS")
    print("------")
    print("EON Core      : ONLINE")
    print("Command System: ONLINE")
    print("Security      : ACTIVE")
    print("Memory        : STANDBY")
    print("Voice         : OFFLINE")
    print("Vision        : OFFLINE")
    print("AI Brain      : NOT CONNECTED")

    print("\nCOMPUTER")
    print("--------")
    print(f"System       : {status['System']}")
    print(f"Release      : {status['Release']}")
    print(f"Machine      : {status['Machine']}")
    print(f"Processor    : {status['Processor']}")
    print(f"Python       : {status['Python']}")

    print("\n" + "=" * 50)


def show_help():
    """Display available commands."""
    print("\nEON COMMANDS")
    print("------------")
    print("help      - Show available commands")
    print("status    - Show EON system status")
    print("time      - Show current time")
    print("clear     - Clear the terminal")
    print("about     - About EON")
    print("exit      - Shut down EON")


def show_about():
    """Display information about EON."""
    print("\n" + "=" * 50)
    print("                    E O N")
    print("         Executive Orchestration Network")
    print("=" * 50)

    print("\nEON is being built as a modular")
    print("personal AI computing system.")

    print("\nFuture systems:")
    print("  [ ] AI Brain")
    print("  [ ] Voice")
    print("  [ ] Voice Authentication")
    print("  [ ] Memory")
    print("  [ ] Agents")
    print("  [ ] Vision")
    print("  [ ] Web Intelligence")
    print("  [ ] Computer Control")
    print("  [ ] Minimalist EON Interface")
    print("  [ ] ESP32 / Hardware Integration")

    print("\nCurrent Version:", VERSION)
    print("=" * 50)


def process_command(command):
    """Process a command given to EON."""

    command = command.lower().strip()

    if command == "":
        return True

    if command == "help":
        show_help()

    elif command == "status":
        show_status()

    elif command == "time":
        current_time = datetime.now().strftime("%I:%M:%S %p")
        print(f"\nEON: The current time is {current_time}.")

    elif command == "clear":
        clear_screen()

    elif command == "about":
        show_about()

    elif command in ["exit", "quit", "shutdown"]:
        print("\nEON: Shutting down.")
        print("EON: See you soon.")
        return False

    else:
        print(f"\nEON: I received: \"{command}\"")
        print("EON: I don't have the capability to execute that yet.")

    return True


def start_eon():
    """Start the EON system."""

    clear_screen()

    print("=" * 50)
    print("                    E O N")
    print("         Executive Orchestration Network")
    print("=" * 50)

    print("\n             ● EON CORE ONLINE")
    print("\n        \"Awaiting your command...\"")

    print("\nType 'help' to see available commands.")
    print("=" * 50)

    running = True

    while running:
        try:
            command = input("\nYOU > ")
            running = process_command(command)

        except KeyboardInterrupt:
            print("\n\nEON: Shutdown requested.")
            running = False

        except Exception as error:
            print("\nEON: An unexpected error occurred.")
            print(f"Details: {error}")

    print("\nEON OFFLINE.")


# ============================================================
#                       PROGRAM START
# ============================================================

if __name__ == "__main__":
    start_eon()
