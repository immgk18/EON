"""
EON Security
============
Permission, confirmation, and activity-control layer.

Security levels:
- SAFE       -> Can run automatically
- PROTECTED  -> Requires user confirmation
- BLOCKED    -> Never allowed through normal EON execution

Important:
High-alert / Kill Mode does NOT disable security.
"""

from datetime import datetime


class Security:
    """Controls permissions and protected actions."""

    # =========================================================
    # ACTION LEVELS
    # =========================================================

    SAFE_ACTIONS = {
        "calculator",
        "system_info",
        "list_files",
        "read_file",
        "web_search",
        "create_task",
        "list_tasks",
        "agent_task",
        "open_application",
        "open_folder",
    }

    PROTECTED_ACTIONS = {
        "delete_file",
        "modify_file",
        "install_software",
        "uninstall_software",
        "send_message",
        "send_email",
        "execute_command",
        "change_system_setting",
        "shutdown_system",
        "move_file",
        "rename_file",
    }

    BLOCKED_ACTIONS = {
        "disable_security",
        "bypass_authentication",
        "bypass_password",
        "bypass_device_lock",
        "steal_credentials",
    }

    def __init__(
        self,
        require_confirmation=True
    ):

        self.enabled = True

        self.require_confirmation = (
            require_confirmation
        )

        self.activity_log = []

        self.session_id = (
            datetime.now().strftime(
                "%Y%m%d%H%M%S"
            )
        )

    # =========================================================
    # ACTION LEVEL
    # =========================================================

    def get_action_level(self, action):

        if not action:
            return "BLOCKED"

        action = action.lower().strip()

        if action in self.BLOCKED_ACTIONS:
            return "BLOCKED"

        if action in self.PROTECTED_ACTIONS:
            return "PROTECTED"

        if action in self.SAFE_ACTIONS:
            return "SAFE"

        # Unknown actions are treated cautiously.
        return "PROTECTED"

    # =========================================================
    # PERMISSION CHECK
    # =========================================================

    def check_permission(self, action):

        if not self.enabled:
            return False

        level = self.get_action_level(
            action
        )

        if level == "BLOCKED":
            return False

        if level == "SAFE":
            return True

        if level == "PROTECTED":
            return False

        return False

    # =========================================================
    # CONFIRMATION
    # =========================================================

    def request_confirmation(self, action):

        if not action:
            return False

        level = self.get_action_level(
            action
        )

        # Blocked actions never receive
        # a normal confirmation bypass.
        if level == "BLOCKED":

            self.log_activity(
                action,
                "BLOCKED",
                "Action is prohibited."
            )

            return False

        if not self.require_confirmation:

            self.log_activity(
                action,
                "AUTO_APPROVED",
                "Confirmation disabled by configuration."
            )

            return True

        print()
        print(
            "========================================"
        )
        print(
            "             EON SECURITY"
        )
        print(
            "========================================"
        )

        print(
            f"Requested action : {action}"
        )

        print(
            f"Security level   : {level}"
        )

        print(
            "Confirmation required."
        )

        print(
            "========================================"
        )

        answer = input(
            "Allow this action? [y/N]: "
        ).strip().lower()

        if answer in {
            "y",
            "yes"
        }:

            self.log_activity(
                action,
                "APPROVED",
                "User approved the action."
            )

            return True

        self.log_activity(
            action,
            "DENIED",
            "User denied the action."
        )

        return False

    # =========================================================
    # AUTHORIZE
    # =========================================================

    def authorize(self, action):

        if not action:

            return False

        level = self.get_action_level(
            action
        )

        # -----------------------------------------------------
        # BLOCKED
        # -----------------------------------------------------

        if level == "BLOCKED":

            self.log_activity(
                action,
                "BLOCKED",
                "Action is not permitted."
            )

            return False

        # -----------------------------------------------------
        # SAFE
        # -----------------------------------------------------

        if level == "SAFE":

            self.log_activity(
                action,
                "ALLOWED",
                "Safe action."
            )

            return True

        # -----------------------------------------------------
        # PROTECTED
        # -----------------------------------------------------

        if level == "PROTECTED":

            return self.request_confirmation(
                action
            )

        return False

    # =========================================================
    # LOG ACTIVITY
    # =========================================================

    def log_activity(
        self,
        action,
        result,
        details=""
    ):

        self.activity_log.append(
            {
                "timestamp":
                    datetime.now().isoformat(),

                "session_id":
                    self.session_id,

                "action":
                    action,

                "result":
                    result,

                "details":
                    details,
            }
        )

    # =========================================================
    # ACTIVITY LOG
    # =========================================================

    def get_activity_log(self):

        return self.activity_log.copy()

    # =========================================================
    # RECENT ACTIVITY
    # =========================================================

    def get_recent_activity(
        self,
        count=10
    ):

        if count <= 0:
            return []

        return self.activity_log[
            -count:
        ]

    # =========================================================
    # CLEAR ACTIVITY
    # =========================================================

    def clear_activity_log(self):

        self.activity_log.clear()

    # =========================================================
    # ENABLE
    # =========================================================

    def enable(self):

        self.enabled = True

        self.log_activity(
            "security_system",
            "ENABLED",
            "Security system enabled."
        )

    # =========================================================
    # DISABLE
    # =========================================================

    def disable(self):

        """
        Security cannot be disabled through normal
        EON operation.

        Kept as a compatibility method so existing
        code does not break.
        """

        self.log_activity(
            "security_system",
            "BLOCKED",
            "Security cannot be disabled through EON."
        )

        return False

    # =========================================================
    # STATUS
    # =========================================================

    def status(self):

        return {
            "enabled":
                self.enabled,

            "confirmation_required":
                self.require_confirmation,

            "safe_actions":
                len(self.SAFE_ACTIONS),

            "protected_actions":
                len(self.PROTECTED_ACTIONS),

            "blocked_actions":
                len(self.BLOCKED_ACTIONS),

            "logged_events":
                len(self.activity_log),

            "session_id":
                self.session_id,

            "status":
                "ONLINE",
        }
