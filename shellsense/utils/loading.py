"""
Module for displaying loading animations and status messages.
"""

import sys
import threading
import time
from typing import Optional


class FuturisticLoading:
    """
    A class for displaying futuristic loading animations and status messages.
    """

    def __init__(self):
        """Initialize the loading animation."""
        self.is_loading = False
        self.loading_thread: Optional[threading.Thread] = None
        self.current_text = ""
        self.current_color = ""

        # ANSI color codes
        self.colors = {
            "RED": "\033[91m",
            "GREEN": "\033[92m",
            "YELLOW": "\033[93m",
            "BLUE": "\033[94m",
            "MAGENTA": "\033[95m",
            "CYAN": "\033[96m",
            "WHITE": "\033[97m",
            "RESET": "\033[0m",
        }

        # Loading animation frames
        self.frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def _animate(self):
        """Internal method to handle the loading animation."""
        frame_idx = 0
        while self.is_loading:
            color = self.colors.get(self.current_color, self.colors["WHITE"])
            frame = self.frames[frame_idx]
            sys.stdout.write(
                f"\r{color}{frame} {self.current_text}{self.colors['RESET']}"
            )
            sys.stdout.flush()
            frame_idx = (frame_idx + 1) % len(self.frames)
            time.sleep(0.1)

    def start(self, text: str, color: str = "WHITE"):
        """
        Start the loading animation.

        Args:
            text (str): Text to display alongside the animation.
            color (str): Color of the text (RED, GREEN, BLUE, etc.).
        """
        self.current_text = text
        self.current_color = color
        self.is_loading = True
        self.loading_thread = threading.Thread(target=self._animate)
        self.loading_thread.daemon = True
        self.loading_thread.start()

    def text(self, text: str, color: str = "WHITE"):
        """
        Update the loading text.

        Args:
            text (str): New text to display.
            color (str): Color of the text.
        """
        self.current_text = text
        self.current_color = color

    def stop(self, final_text: str = "", color: str = "WHITE"):
        """
        Stop the loading animation.

        Args:
            final_text (str): Final text to display.
            color (str): Color of the final text.
        """
        self.is_loading = False
        if self.loading_thread:
            self.loading_thread.join()
        if final_text:
            color_code = self.colors.get(color, self.colors["WHITE"])
            sys.stdout.write(f"\r{color_code}{final_text}{self.colors['RESET']}\n")
        else:
            sys.stdout.write("\r")
        sys.stdout.flush()

    def clear(self):
        """Clear the current line in the terminal."""
        sys.stdout.write("\r\033[K")
        sys.stdout.flush()
