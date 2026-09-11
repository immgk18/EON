"""
EON Computer Control
====================
Controlled computer interaction layer for EON.

Capabilities:
- System information
- Open approved applications
- Open approved/safe folders
- Check application availability
- Controlled actions through EON Security

EON does NOT provide unrestricted shell execution.
"""

import os
import platform
import subprocess
from pathlib import Path


class ComputerController:
    """Controls approved computer operations."""

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(self, security=None):

        self.security = security

        self.enabled = True

        self.last_action = None
        self.last_result = None

        # -----------------------------------------------------
        # Windows application allowlist
        # -----------------------------------------------------

        self.allowed_apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
        }

        # -----------------------------------------------------
        # Common folders
        # -----------------------------------------------------

        self.allowed_special_folders = {
            "desktop": Path.home() / "Desktop",
            "documents": Path.home() / "Documents",
            "downloads": Path.home() / "Downloads",
            "pictures": Path.home() / "Pictures",
            "videos": Path.home() / "Videos",
        }

    # =========================================================
    # SECURITY
    # =========================================================

    def _authorize(self, action, details=None):

        if self.security is None:

            # Fail closed when security is unavailable.
            return False

        return self.security.authorize(
            action,
            details or {}
        )

    # =========================================================
    # ENABLE / DISABLE
    # =========================================================

    def enable(self):

        self.enabled = True

        return True

    def disable(self):

        self.enabled = False

        return True

    # =========================================================
    # SYSTEM INFORMATION
    # =========================================================

    def system_info(self):

        return {
            "operating_system":
                platform.system(),

            "os_version":
                platform.version(),

            "release":
                platform.release(),

            "machine":
                platform.machine(),

            "processor":
                platform.processor(),

            "python":
                platform.python_version(),

            "computer_name":
                platform.node(),
        }

    # =========================================================
    # APPLICATIONS
    # =========================================================

    def get_allowed_applications(self):

        return list(
            self.allowed_apps.keys()
        )

    def is_application_allowed(
        self,
        application
    ):

        if not application:

            return False

        return (
            application.lower().strip()
            in self.allowed_apps
        )

    def open_application(
        self,
        application
    ):

        if not self.enabled:

            return {
                "success": False,
                "error":
                    "Computer control is disabled.",
            }

        if not application:

            return {
                "success": False,
                "error":
                    "No application specified.",
            }

        application = (
            application.lower().strip()
        )

        if not self.is_application_allowed(
            application
        ):

            return {
                "success": False,
                "error":
                    f"Application '{application}' "
                    "is not on the EON allowlist.",
            }

        # -----------------------------------------------------
        # Security authorization
        # -----------------------------------------------------

        authorized = self._authorize(
            "open_application",
            {
                "application":
                    application
            }
        )

        if not authorized:

            return {
                "success": False,
                "error":
                    "Security authorization denied.",
            }

        executable = self.allowed_apps[
            application
        ]

        try:

            if platform.system() == "Windows":

                process = subprocess.Popen(
                    [executable],
                    shell=False
                )

            else:

                process = subprocess.Popen(
                    [executable],
                    shell=False
                )

            self.last_action = (
                f"open_application:{application}"
            )

            self.last_result = {
                "success": True,
                "application":
                    application,
            }

            return self.last_result

        except (
            FileNotFoundError,
            OSError
        ) as error:

            self.last_result = {
                "success": False,
                "error":
                    f"Unable to open application: "
                    f"{error}",
            }

            return self.last_result

    # =========================================================
    # FOLDER RESOLUTION
    # =========================================================

    def resolve_folder(
        self,
        folder
    ):

        if not folder:

            return None

        folder = folder.lower().strip()

        if folder in self.allowed_special_folders:

            path = self.allowed_special_folders[
                folder
            ]

            return path

        # -----------------------------------------------------
        # Only allow an explicitly existing directory.
        # -----------------------------------------------------

        candidate = Path(folder).expanduser()

        try:

            candidate = candidate.resolve()

        except OSError:

            return None

        if candidate.exists() and candidate.is_dir():

            return candidate

        return None

    # =========================================================
    # OPEN FOLDER
    # =========================================================

    def open_folder(
        self,
        folder
    ):

        if not self.enabled:

            return {
                "success": False,
                "error":
                    "Computer control is disabled.",
            }

        path = self.resolve_folder(
            folder
        )

        if path is None:

            return {
                "success": False,
                "error":
                    "Folder is not available "
                    "through the controlled interface.",
            }

        authorized = self._authorize(
            "open_folder",
            {
                "folder":
                    str(path)
            }
        )

        if not authorized:

            return {
                "success": False,
                "error":
                    "Security authorization denied.",
            }

        try:

            if platform.system() == "Windows":

                os.startfile(str(path))

            elif platform.system() == "Darwin":

                subprocess.Popen(
                    ["open", str(path)],
                    shell=False
                )

            else:

                subprocess.Popen(
                    ["xdg-open", str(path)],
                    shell=False
                )

            self.last_action = (
                f"open_folder:{path}"
            )

            self.last_result = {
                "success": True,
                "folder":
                    str(path),
            }

            return self.last_result

        except OSError as error:

            self.last_result = {
                "success": False,
                "error":
                    f"Unable to open folder: "
                    f"{error}",
            }

            return self.last_result

    # =========================================================
    # CHECK PATH
    # =========================================================

    def path_exists(
        self,
        path
    ):

        if not path:

            return False

        try:

            return Path(
                path
            ).expanduser().exists()

        except OSError:

            return False

    # =========================================================
    # GET PATH INFORMATION
    # =========================================================

    def path_info(
        self,
        path
    ):

        if not path:

            return None

        try:

            target = (
                Path(path)
                .expanduser()
                .resolve()
            )

            if not target.exists():

                return None

            return {
                "name":
                    target.name,

                "path":
                    str(target),

                "type":
                    "directory"
                    if target.is_dir()
                    else "file",

                "size":
                    target.stat().st_size,
            }

        except OSError:

            return None

    # =========================================================
    # LAST ACTION
    # =========================================================

    def get_last_action(self):

        return self.last_action

    def get_last_result(self):

        return self.last_result

    # =========================================================
    # STATUS
    # =========================================================

    def status(self):

        return {
            "enabled":
                self.enabled,

            "platform":
                platform.system(),

            "allowed_applications":
                self.get_allowed_applications(),

            "security_connected":
                self.security is not None,

            "last_action":
                self.last_action,

            "status":
                "ONLINE"
                if self.enabled
                else "DISABLED",
        }
