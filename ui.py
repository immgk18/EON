"""
EON UI
======
Lightweight visual interface for EON.

Supports:
- Normal mode
- High-alert / Kill mode
- Idle state
- Listening state
- Thinking state
- Speaking state
- Alert state
- Terminal-safe rendering

This module does not bypass security or system controls.
"""

import os
import sys
import time


class UI:
    """EON visual interface controller."""

    MODES = {
        "NORMAL",
        "KILL",
    }

    STATES = {
        "IDLE",
        "LISTENING",
        "THINKING",
        "SPEAKING",
        "ALERT",
    }

    def __init__(self):

        self.enabled = True

        self.mode = "NORMAL"
        self.state = "IDLE"

        self.theme = "DARK"
        self.orb_color = "GOLD"

        self.caption = "EON STANDBY"

        self.animation_enabled = True

    # =========================================================
    # MODE
    # =========================================================

    def set_mode(self, mode):

        if not mode:
            return False

        mode = mode.upper().strip()

        if mode not in self.MODES:
            return False

        self.mode = mode

        if mode == "KILL":
            self.caption = "HIGH-ALERT MODE"

        else:
            self.caption = "EON STANDBY"

        return True

    # =========================================================
    # STATE
    # =========================================================

    def set_state(self, state):

        if not state:
            return False

        state = state.upper().strip()

        if state not in self.STATES:
            return False

        self.state = state

        return True

    # =========================================================
    # VISUAL STATES
    # =========================================================

    def idle(self):

        self.set_state("IDLE")

        self.caption = "EON STANDBY"

        self.render()

    def listening(self):

        self.set_state("LISTENING")

        self.caption = "LISTENING..."

        self.render()

    def thinking(self):

        self.set_state("THINKING")

        self.caption = "THINKING..."

        self.render()

    def speaking(self):

        self.set_state("SPEAKING")

        self.caption = "SPEAKING..."

        self.render()

    def alert(self):

        self.set_state("ALERT")

        self.caption = "HIGH-ALERT"

        self.render()

    # =========================================================
    # ORB
    # =========================================================

    def get_orb(self):

        if self.mode == "KILL":

            return "◉"

        if self.state == "LISTENING":

            return "◉"

        if self.state == "THINKING":

            return "◎"

        if self.state == "SPEAKING":

            return "◉"

        if self.state == "ALERT":

            return "◉"

        return "◉"

    # =========================================================
    # RENDER
    # =========================================================

    def render(self):

        if not self.enabled:
            return

        orb = self.get_orb()

        print()
        print(
            "╔══════════════════════════════╗"
        )

        print(
            "║             E O N            ║"
        )

        print(
            "║                              ║"
        )

        print(
            f"║              {orb}               ║"
        )

        print(
            "║                              ║"
        )

        print(
            f"║      {self.caption:^20}      ║"
        )

        print(
            "║                              ║"
        )

        print(
            f"║ MODE: {self.mode:<22}║"
        )

        print(
            f"║ STATE: {self.state:<21}║"
        )

        print(
            "╚══════════════════════════════╝"
        )

    # =========================================================
    # CLEAR SCREEN
    # =========================================================

    def clear(self):

        try:

            if os.name == "nt":

                os.system("cls")

            else:

                os.system("clear")

        except Exception:

            print("\n" * 5)

    # =========================================================
    # HEADER
    # =========================================================

    def header(self):

        print(
            "===================================="
        )

        print(
            "              E O N"
        )

        print(
            "   Executive Orchestration Network"
        )

        print(
            "===================================="
        )

    # =========================================================
    # ANIMATION
    # =========================================================

    def animation_frame(self, frame=0):

        frames = [
            "◉",
            "◎",
            "○",
            "◎",
        ]

        return frames[
            frame % len(frames)
        ]

    def animate(
        self,
        duration=1.0,
        interval=0.15
    ):

        if not self.animation_enabled:
            return

        start = time.time()

        frame = 0

        while (
            time.time() - start
            < duration
        ):

            orb = self.animation_frame(
                frame
            )

            sys.stdout.write(
                f"\rEON {orb} "
                f"{self.caption}"
            )

            sys.stdout.flush()

            time.sleep(interval)

            frame += 1

        print()

    # =========================================================
    # SHOW MESSAGE
    # =========================================================

    def show(
        self,
        message
    ):

        if message is None:
            return

        print(
            f"EON > {message}"
        )

    # =========================================================
    # STATUS
    # =========================================================

    def status(self):

        return {

            "enabled":
                self.enabled,

            "mode":
                self.mode,

            "state":
                self.state,

            "theme":
                self.theme,

            "orb_color":
                self.orb_color,

            "caption":
                self.caption,

            "animation":
                self.animation_enabled,

        }

    # =========================================================
    # RESET
    # =========================================================

    def reset(self):

        self.mode = "NORMAL"

        self.state = "IDLE"

        self.caption = "EON STANDBY"

        return True

    # =========================================================
    # SHUTDOWN
    # =========================================================

    def shutdown(self):

        self.state = "IDLE"

        self.caption = "EON OFFLINE"

        print()
        print(
            "EON > UI OFFLINE."
        )

        return True
