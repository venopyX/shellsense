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

# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Print the futuristic art with colors and animation
print_with_animation(colors['cyan'] + art + colors['reset'])

# Add a futuristic message
message = "Welcome to the future of Terminal!"
print_with_animation(colors['green'] + message + colors['reset'], delay=0.1)
