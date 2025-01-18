#!/bin/bash

echo "Installing Python dependencies..."

# Use --break-system-packages to handle externally managed environments
pip3 install -r requirements.txt --break-system-packages

# if [[ "$(python3 -V 2>&1)" < "Python 3.8" ]]; then
#     echo "Python 3.8 or higher is required. Please update your Python version."
#     exit 1
# fi

if [ $? -ne 0 ]; then
    echo "Error: Unable to install dependencies. Please ensure pip is correctly installed."
    exit 1
fi

echo "Adding ShellSense to .zshrc..."

# Dynamically detect plugin directory and set up aliases
PLUGIN_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
if ! grep -q "source $PLUGIN_DIR/zsh/load_plugin.zsh" ~/.zshrc; then
    echo "source $PLUGIN_DIR/zsh/load_plugin.zsh" >> ~/.zshrc
    echo "ShellSense plugin added to .zshrc."
else
    echo "ShellSense plugin already configured in .zshrc."
fi

echo "Setup complete. Restart your terminal or run 'source ~/.zshrc' to activate ShellSense."
