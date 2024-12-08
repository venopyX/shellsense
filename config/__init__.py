import time
import sys
import os

# ANSI escape codes for colors
colors = {
    'reset': '\033[0m',
    'blue': '\033[94m',
    'cyan': '\033[96m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'red': '\033[91m',
    'magenta': '\033[95m'
}

# Futuristic ASCII art
art = """
|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
|  _, _,_ __, _,  _,   _, __, _, _  _, __, |
| (_  |_| |_  |   |   (_  |_  |\\ | (_  |_  |
| ,_) | | |_, |_, |_, ,_) |_, | \\| ,_) |_, |
|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
"""

# Function to print with animation
def print_with_animation(text, delay=0.005):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def save_cursor_position():
    # ANSI escape code to save the current cursor position
    sys.stdout.write('\033[s')
    sys.stdout.flush()

def restore_cursor_position():
    # ANSI escape code to restore the saved cursor position
    sys.stdout.write('\033[u')
    sys.stdout.flush()

def move_cursor_to_top():
    # ANSI escape code to move the cursor to the top of the terminal
    sys.stdout.write('\033[H')
    sys.stdout.flush()

# Clear the terminal
# os.system('cls' if os.name == 'nt' else 'clear')
# print("\033[H", end="")
# sys.stdout.write('\033[H')
# sys.stdout.flush()
# save_cursor_position()

# move_cursor_to_top()

# Print the futuristic art with colors and animation
print_with_animation(colors['cyan'] + art + colors['reset'])

# Add a futuristic message
message = "Welcome to the future of Terminal!"
print_with_animation(colors['green'] + message + colors['reset'], delay=0.1)
