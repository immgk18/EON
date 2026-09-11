"""
EON User Interface
==================
Visual state and presentation layer for EON.

Design:
- Dark / minimal interface
- Central EON orb
- System states
- NORMAL and KILL modes
- Small status captions
- No heavy GUI dependency

A graphical desktop/mobile UI can be connected
to this interface later.
"""

import os
import sys
import time


class EONUI:
    """Controls EON's visual interface state."""

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(self):

        self.mode = "NORMAL"

        self.state = "IDLE"

        self.running = True

        self.states = {
            "IDLE": "EON STANDBY",
            "LISTENING": "LISTENING",
            "THINKING": "THINKING",
            "SPEAKING": "SPEAKING",
            "ALERT": "HIGH ALERT",
        }

        self.mode_descriptions = {
            "NORMAL":
                "EON HAS LIMITS",

            "KILL":
                "LIMITERS... RELEASED",
        }

        self.orbs = {
            "NORMAL": {
                "IDLE": "●",
                "LISTENING": "◉",
                "THINKING": "◉",
                "SPEAKING": "◉",
                "ALERT": "◉",
            },

            "KILL": {
                "IDLE": "◉",
                "LISTENING": "◎",
                "THINKING": "◎",
                "SPEAKING": "◎",
                "ALERT": "◉",
            },
        }

    # =========================================================
    # STATE MANAGEMENT
    # =========================================================

    def set_state(self, state):

        if not state:

            self.state = "IDLE"

            return

        state = state.upper().strip()

        if state not in self.states:

            state = "IDLE"

        self.state = state

    def get_state(self):

        return self.state

    # =========================================================
    # MODE MANAGEMENT
    # =========================================================

    def set_mode(self, mode):

        if not mode:

            self.mode = "NORMAL"

            return

        mode = mode.upper().strip()

        if mode not in {"NORMAL", "KILL"}:

            mode = "NORMAL"

        self.mode = mode

        # High-alert mode gets ALERT state.
        if mode == "KILL":

            self.set_state("ALERT")

        else:

            self.set_state("IDLE")

    def get_mode(self):

        return self.mode

    # =========================================================
    # ORB
    # =========================================================

    def get_orb(self):

        return self.orbs[
            self.mode
        ][
            self.state
        ]

    # =========================================================
    # CAPTION
    # =========================================================

    def get_caption(self):

        if self.mode == "KILL":

            return "EON HIGH-ALERT"

        return self.states[
            self.state
        ]

    # =========================================================
    # CLEAR SCREEN
    # =========================================================

    def clear_screen(self):

        if sys.platform.startswith("win"):

            os.system("cls")

        else:

            os.system("clear")

    # =========================================================
    # HEADER
    # =========================================================

    def render_header(self):

        return (
            "========================================\n"
            "                 E O N                  \n"
            "     EXECUTIVE ORCHESTRATION NETWORK    \n"
            "========================================"
        )

    # =========================================================
    # ORB RENDER
    # =========================================================

    def render_orb(self):

        orb = self.get_orb()

        return (
            "\n"
            "                 ╱╲\n"
            f"                 {orb}\n"
            "                 ╲╱\n"
        )

    # =========================================================
    # MAIN RENDER
    # =========================================================

    def render(self):

        caption = self.get_caption()

        mode_description = (
            self.mode_descriptions[
                self.mode
            ]
        )

        return (
            "\n"
            + self.render_header()
            + "\n"
            + self.render_orb()
            + "\n"
            f"              {caption}\n"
            f"              MODE: {self.mode}\n"
            f"              {mode_description}\n"
            "\n"
        )

    # =========================================================
    # DISPLAY
    # =========================================================

    def show(self):

        print(
            self.render()
        )

    # =========================================================
    # VISUAL STATES
    # =========================================================

    def idle(self):

        self.set_state("IDLE")

        self.show()

    def listening(self):

        self.set_state("LISTENING")

        self.show()

    def thinking(self):

        self.set_state("THINKING")

        self.show()

    def speaking(self):

        self.set_state("SPEAKING")

        self.show()

    def alert(self):

        self.set_state("ALERT")

        self.show()

    # =========================================================
    # ANIMATION FRAME
    # =========================================================

    def animation_frame(
        self,
        frame=0
    ):
        """
        Generate a lightweight animated orb frame.

        This is intentionally terminal-safe.
        A graphical renderer can replace this later.
        """

        normal_frames = [
            "·",
            "•",
            "●",
            "◉",
            "●",
            "•",
        ]

        kill_frames = [
            "·",
            "○",
            "◎",
            "◉",
            "◎",
            "○",
        ]

        frames = (
            kill_frames
            if self.mode == "KILL"
            else normal_frames
        )

        orb = frames[
            frame % len(frames)
        ]

        return (
            "\n"
            "                 ╱╲\n"
            f"                 {orb}\n"
            "                 ╲╱\n"
        )

    def animate(
        self,
        frames=6,
        delay=0.08
    ):
        """
        Run a small terminal animation.
        """

        for frame in range(frames):

            self.clear_screen()

            print(
                self.render_header()
            )

            print(
                self.animation_frame(
                    frame
                )
            )

            print(
                f"              {self.get_caption()}"
            )

            print(
                f"              MODE: {self.mode}"
            )

            time.sleep(delay)

    # =========================================================
    # STATUS
    # =========================================================

    def status(self):

        return {
            "mode":
                self.mode,

            "state":
                self.state,

            "caption":
                self.get_caption(),

            "orb":
                self.get_orb(),

            "running":
                self.running,

            "status":
                "ONLINE",
        }

    # =========================================================
    # SHUTDOWN
    # =========================================================

    def shutdown(self):

        self.running = False

        self.set_state("IDLE")

        return True
