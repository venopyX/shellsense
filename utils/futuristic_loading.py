import sys
import time
import itertools
from threading import Thread

# Color codes
RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BLUE = "\033[94m"
MAGENTA = "\033[35m"
WHITE = "\033[97m"

# Map of color names to their corresponding color codes
COLOR_MAP = {
    "RESET": RESET,
    "GREEN": GREEN,
    "YELLOW": YELLOW,
    "RED": RED,
    "CYAN": CYAN,
    "BLUE": BLUE,
    "MAGENTA": MAGENTA,
    "WHITE": WHITE
}

class FuturisticLoading:
    def __init__(self, symbols=None, sleep_time=0.2):
        self.symbols = symbols or ['⏳', '⚡', '🔮', '🌀', '🌟']
        self.sleep_time = sleep_time
        self.done = False
        self.thread = None
        self.message = ""
        self.color = RESET

    def _get_color_code(self, color):
        """Get the color code from either a color string or a raw code."""
        if color in COLOR_MAP:
            return COLOR_MAP[color]
        elif color.startswith("\033["):
            return color
        else:
            return RESET

    def start(self, initial_message="Loading", color=RESET):
        """Start the loading animation with the initial message and color."""
        self.done = False
        self.message = initial_message
        self.color = self._get_color_code(color)
        self.thread = Thread(target=self._animate)
        self.thread.start()

    def _animate(self):
        """Animate the loading symbols."""
        symbol_cycle = itertools.cycle(self.symbols)
        while not self.done:
            current_symbol = next(symbol_cycle)
            sys.stdout.write(f'\r{self.color}{self.message} {current_symbol}   {RESET}')
            sys.stdout.flush()
            time.sleep(self.sleep_time)

    def text(self, new_message, color=RESET):
        """Update the displayed message and color during the animation."""
        self.message = new_message
        self.color = self._get_color_code(color)

    def stop(self, final_message="Done! ✅", color=GREEN):
        """Stop the animation and display the final message with the specified color."""
        self.done = True
        self.thread.join()
        sys.stdout.write(f'\r{self._get_color_code(color)}{final_message}{RESET}\n')

    def clear(self):
        """Delete the last line in the terminal output."""
        sys.stdout.write('\x1b[1A')  # Move cursor up one line
        sys.stdout.write('\x1b[2K')  # Clear the entire line
        sys.stdout.flush()

# # # Usage example:
# if __name__ == "__main__":
#     loader = FuturisticLoading()

#     loader.start("Starting... 🚀", "CYAN")
#     time.sleep(1)
#     loader.text("Processing... ⏳", "CYAN")
#     time.sleep(2)
#     loader.text("Downloading... 📥", "CYAN")
#     time.sleep(2)
#     loader.text("Saving... 💾", "CYAN")
#     time.sleep(1)
#     loader.text("Saved! ✅", GREEN)
#     time.sleep(1)
#     loader.stop("Completed! 🎉", GREEN)

#     # Stop the loader before clearing the text from the terminal
#     loader.stop()
#     loader.clear()

#     loader.start("Error: Download Failed! ❌", "RED")
#     time.sleep(1)
#     loader.stop("Retrying... 🔄", "CYAN")
#     loader.clear()
