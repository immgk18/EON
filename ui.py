"""
EON User Interface
==================
Minimal visual interface for EON.

Design:
- Black background
- Radiant golden orb
- Small status text
- Different visual states
"""


class EONUI:
    """Controls EON's visual interface."""

    def __init__(self):
        self.mode = "NORMAL"
        self.state = "IDLE"

        self.states = {
            "IDLE": "EON STANDBY",
            "LISTENING": "LISTENING",
            "THINKING": "THINKING",
            "SPEAKING": "SPEAKING",
            "ALERT": "HIGH ALERT",
        }

    # ─────────────────────────────────────
    # STATE CONTROL
    # ─────────────────────────────────────

    def set_state(self, state):
        """Change the visual state."""

        state = state.upper()

        if state not in self.states:
            state = "IDLE"

        self.state = state

    def set_mode(self, mode):
        """Change EON's visual mode."""

        mode = mode.upper()

        if mode not in {"NORMAL", "KILL"}:
            mode = "NORMAL"

        self.mode = mode

    # ─────────────────────────────────────
    # DISPLAY
    # ─────────────────────────────────────

    def render(self):
        """Return the current UI representation."""

        if self.mode == "KILL":
            orb = "◉"
            caption = "EON HIGH-ALERT"
        else:
            orb = "●"
            caption = self.states[self.state]

        return (
            "\n"
            "          ╔══════════════╗\n"
            "                 " + orb + "\n"
            "          ╚══════════════╝\n"
            "\n"
            f"              {caption}\n"
            f"              MODE: {self.mode}\n"
        )

    def show(self):
        """Display the EON interface."""

        print(self.render())

    # ─────────────────────────────────────
    # VISUAL STATES
    # ─────────────────────────────────────

    def idle(self):
        """Set EON to idle."""

        self.set_state("IDLE")
        self.show()

    def listening(self):
        """Set EON to listening."""

        self.set_state("LISTENING")
        self.show()

    def thinking(self):
        """Set EON to thinking."""

        self.set_state("THINKING")
        self.show()

    def speaking(self):
        """Set EON to speaking."""

        self.set_state("SPEAKING")
        self.show()

    def alert(self):
        """Set EON to high alert."""

        self.set_state("ALERT")
        self.show()

    # ─────────────────────────────────────
    # STATUS
    # ─────────────────────────────────────

    def status(self):
        """Return UI status."""

        return {
            "mode": self.mode,
            "state": self.state,
            "caption": self.states[self.state],
            "status": "ONLINE",
        }
