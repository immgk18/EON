"""
EON Security
============
Permission, confirmation, and activity-control layer for EON.
"""


class Security:
    """Controls permissions for EON actions."""

    def __init__(self, require_confirmation=True):
        self.enabled = True
        self.require_confirmation = require_confirmation

        # Actions that should always require user confirmation.
        self.protected_actions = {
            "delete_file",
            "modify_file",
            "install_software",
            "uninstall_software",
            "send_message",
            "send_email",
            "execute_command",
            "change_system_setting",
            "shutdown_system",
        }

        self.activity_log = []

    def check_permission(self, action):
        """
        Check whether an action requires confirmation.

        Returns:
            True  -> action may proceed
            False -> confirmation is required
        """

        if not self.enabled:
            return True

        if action in self.protected_actions:
            return False

        return True

    def request_confirmation(self, action):
        """
        Ask the user for confirmation before a protected action.
        """

        if not self.require_confirmation:
            return True

        print()
        print("EON SECURITY")
        print("----------------------------")
        print(f"Requested action: {action}")
        print("Confirmation required.")
        print("----------------------------")

        answer = input("Allow this action? [y/N]: ").strip().lower()

        if answer in {"y", "yes"}:
            self.log_activity(
                action,
                "APPROVED"
            )
            return True

        self.log_activity(
            action,
            "DENIED"
        )

        return False

    def authorize(self, action):
        """
        Main authorization interface.

        Safe actions can proceed directly.
        Protected actions require confirmation.
        """

        if self.check_permission(action):
            self.log_activity(
                action,
                "ALLOWED"
            )
            return True

        return self.request_confirmation(action)

    def log_activity(self, action, result):
        """Record an EON security event."""

        self.activity_log.append({
            "action": action,
            "result": result
        })

    def get_activity_log(self):
        """Return the security activity log."""

        return self.activity_log.copy()

    def clear_activity_log(self):
        """Clear the current security activity log."""

        self.activity_log.clear()

    def enable(self):
        """Enable the security system."""

        self.enabled = True

    def disable(self):
        """
        Disable the security system.

        This method exists for development/testing only.
        Protected operations should remain confirmation-gated
        in the production system.
        """

        self.enabled = False

    def status(self):
        """Return the current security status."""

        return {
            "enabled": self.enabled,
            "confirmation_required": self.require_confirmation,
            "logged_events": len(self.activity_log),
        }
