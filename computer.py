"""
EON Computer Control
====================
Controlled computer interaction layer for EON.
"""

import os
import platform
import subprocess
from pathlib import Path


class ComputerController:
    """Provides controlled computer operations."""

    def __init__(self, security=None):
        self.security = security
        self.status_state = "ONLINE"

    def system_info(self):
        """Return basic information about the current computer."""

        return {
            "operating_system": platform.system(),
            "os_version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python": platform.python_version(),
        }

    def open_application(self, application):
        """
        Open an application using the operating system.

        Only predefined/common applications are accepted.
        """

        allowed_apps = {
            "notepad": ["notepad.exe"],
            "calculator": ["calc.exe"],
            "paint": ["mspaint.exe"],
        }

        app = application.lower().strip()

        if app not in allowed_apps:
            return (
                f"Application '{application}' is not in "
                "the approved application list."
            )

        if self.security:
            if not self.security.authorize("open_application"):
                return "Action denied by security."

        try:
            subprocess.Popen(
                allowed_apps[app],
                shell=False
            )

            return f"Opening {application}."

        except OSError as error:
            return f"Unable to open application: {error}"

    def open_folder(self, path):
        """Open an approved folder."""

        target = Path(path).expanduser().resolve()

        if not target.exists():
            return "Folder not found."

        if not target.is_dir():
            return "The selected path is not a folder."

        if self.security:
            if not self.security.authorize("open_folder"):
                return "Action denied by security."

        try:
            if platform.system() == "Windows":
                os.startfile(str(target))

            elif platform.system() == "Darwin":
                subprocess.Popen(
                    ["open", str(target)],
                    shell=False
                )

            else:
                subprocess.Popen(
                    ["xdg-open", str(target)],
                    shell=False
                )

            return f"Opening folder: {target}"

        except OSError as error:
            return f"Unable to open folder: {error}"

    def status(self):
        """Return computer controller status."""

        return {
            "status": self.status_state,
            "platform": platform.system(),
            "computer_control": "READY",
        }
