import logging
import sys
import threading
import time
from typing import Optional

logger = logging.getLogger(__name__)


class FuturisticLoading:
    """
    A class for displaying futuristic loading animations in the terminal.
    """

    def __init__(self):
        """Initialize the loading animation."""
        self.loading = False
        self.thread: Optional[threading.Thread] = None
        self.frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
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
        self.current_text = ""

    def _animate(self, text: str, color: str = "WHITE") -> None:
        """
        Animate the loading indicator.

        Args:
            text (str): Text to display alongside the animation
            color (str): Color to use for the text
        """
        try:
            i = 0
            while self.loading:
                frame = self.frames[i % len(self.frames)]
                sys.stdout.write(
                    f"\r{self.colors[color]}{frame} {text}{self.colors['RESET']}"
                )
                sys.stdout.flush()
                time.sleep(0.1)
                i += 1
        except Exception as e:
            logger.error(f"Animation error: {str(e)}")

    def start(self, text: str = "Loading...", color: str = "WHITE") -> None:
        """
        Start the loading animation.

        Args:
            text (str, optional): Text to display. Defaults to "Loading...".
            color (str, optional): Color of the text. Defaults to "WHITE".
        """
        try:
            logger.debug(f"Starting loading animation with text: {text}")
            if not self.loading:
                self.loading = True
                self.current_text = text
                self.thread = threading.Thread(target=self._animate, args=(text, color))
                self.thread.daemon = True
                self.thread.start()
        except Exception as e:
            logger.error(f"Failed to start loading animation: {str(e)}")

    def stop(self, text: Optional[str] = None, color: str = "WHITE") -> None:
        """
        Stop the loading animation.

        Args:
            text (str, optional): Final text to display. If None, clears the line.
            color (str, optional): Color of the final text. Defaults to "WHITE".
        """
        try:
            logger.debug("Stopping loading animation")
            if self.loading:
                self.loading = False
                if self.thread:
                    self.thread.join()
                if text:
                    sys.stdout.write(
                        f"\r{self.colors[color]}{text}{self.colors['RESET']}\n"
                    )
                else:
                    sys.stdout.write("\r\033[K")
                sys.stdout.flush()
        except Exception as e:
            logger.error(f"Failed to stop loading animation: {str(e)}")

    def text(self, text: str, color: str = "WHITE") -> None:
        """
        Update the loading text.

        Args:
            text (str): New text to display
            color (str, optional): Color of the text. Defaults to "WHITE".
        """
        try:
            logger.debug(f"Updating loading text to: {text}")
            self.current_text = text
            sys.stdout.write(f"\r{self.colors[color]}{text}{self.colors['RESET']}")
            sys.stdout.flush()
        except Exception as e:
            logger.error(f"Failed to update loading text: {str(e)}")

    def clear(self) -> None:
        """Clear the current line in the terminal."""
        try:
            logger.debug("Clearing loading text")
            sys.stdout.write("\r\033[K")
            sys.stdout.flush()
        except Exception as e:
            logger.error(f"Failed to clear loading text: {str(e)}")


# Usage example:
if __name__ == "__main__":
    loader = FuturisticLoading()

    loader.start("Starting... ", "CYAN")
    time.sleep(1)
    loader.text("Processing... ", "CYAN")
    time.sleep(2)
    loader.text("Downloading... ", "CYAN")
    time.sleep(2)
    loader.text("Saving... ", "CYAN")
    time.sleep(1)
    loader.text("Saved! ", "GREEN")
    time.sleep(1)
    loader.stop("Completed! ", "GREEN")

    # Stop the loader before clearing the text from the terminal
    loader.stop()
    loader.clear()

    loader.start("Error: Download Failed! ", "RED")
    time.sleep(1)
    loader.stop("Retrying... ", "CYAN")
    loader.clear()
