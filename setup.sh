#!/bin/bash

echo "Installing Python dependencies..."

# Define plugin directory and venv path
PLUGIN_DIR=$(pwd)
VENV_DIR="$PLUGIN_DIR/venv"

# Check if virtual environment exists; if not, create it
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating a Python virtual environment..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Trying system-wide installation with --break-system-packages..."
        pip install -r requirements.txt --break-system-packages
        if [ $? -ne 0 ]; then
            echo "Error: Unable to install dependencies. Please ensure Python and pip are correctly installed."
            exit 1
        fi
    else
        echo "Virtual environment created successfully."
    fi
fi

# Activate the virtual environment and install dependencies
source "$VENV_DIR/bin/activate"
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies in the virtual environment."
    exit 1
fi

echo "Adding ShellSense to .zshrc..."
if ! grep -q "source $PLUGIN_DIR/zsh/load_plugin.zsh" ~/.zshrc; then
    echo "source $PLUGIN_DIR/zsh/load_plugin.zsh" >> ~/.zshrc
fi

echo "Setup complete. Restart your terminal or run 'source ~/.zshrc' to activate ShellSense."
