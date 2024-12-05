import os
import subprocess
from getpass import getpass
from tools.base_tool import BaseTool

class CommandExecutionTool(BaseTool):
    """
    A tool to execute shell commands, create files/folders, and handle operations in the user's home directory.

    Input:
    - commands (list or string): A list of valid shell commands to execute sequentially or a single string containing commands separated by '&&'.
                                  Example: ["mkdir ~/path/foldername", "touch ~/path/filename"] or
                                          "mkdir ~/path/foldername && touch ~/path/filename"
    - confirm_harmful (bool): True if harmful commands flagged by the tool should be executed.

    IMPORTANT:
    - This tool ONLY accepts a list of valid shell commands inside the `commands` parameter or a single string with commands separated by '&&'.
    - The AI MUST NOT create new parameters (e.g., folder_name, file_name) or change the input format.
    - The `commands` parameter should contain shell commands like `mkdir` or `touch`.
    - Don't use 'cd' command since you can't cd into other folder, execute command with path directly instead!

    DANGER NOTICE:
    - ARGUMENTS MUST BE VALID SHELL COMMANDS!
    """

    # List of explicitly excluded commands for security
    EXCLUDED_COMMANDS = ["rm -rf /", "shutdown", "reboot", "dd if=", "mkfs", "wget http://"]

    def invoke(self, input_data: dict) -> dict:
        """
        Execute commands or create files/folders as per user input.

        Args:
            input_data (dict): Dictionary with the following keys:
                - commands (list or string): List of commands to execute (strings), or a single string with commands.
                - confirm_harmful (bool): True if commands are marked as harmful by AI.

        Returns:
            dict: Status of the executed commands, including any errors or skipped commands.
        """
        # Debug: Print the input to ensure it is correctly formatted
        print("Input received:", input_data)

        # Retrieve commands and ensure they are in the correct format (list of commands)
        commands = input_data.get("commands", [])
        confirm_harmful = input_data.get("confirm_harmful", False)

        # If commands is a string, split it into a list of commands
        if isinstance(commands, str):
            commands = self.split_commands(commands)

        if not commands:
            commands = input_data.get("command", [])
            if isinstance(commands, str):
                commands = self.split_commands(commands)
            else:
                return {"error": "No commands provided for execution."}

        # Validate commands for security
        harmful_commands = [cmd for cmd in commands if self.is_harmful_command(cmd)]
        safe_commands = [cmd for cmd in commands if cmd not in harmful_commands]

        # Display commands for user confirmation
        print("Commands to execute:")
        for cmd in commands:
            print(f"- {cmd} {'(Harmful)' if cmd in harmful_commands else ''}")

        if harmful_commands:
            print("\n⚠️ Warning: The following commands are flagged as harmful:")
            for cmd in harmful_commands:
                print(f"- {cmd}")
            if not confirm_harmful:
                print("\nExecution aborted due to harmful commands.")
                return {"error": "Execution aborted. Harmful commands detected."}

        # Prompt for user confirmation
        proceed = input("\nDo you want to execute the commands? (yes/y to proceed, no/n to cancel): ").strip().lower()
        if proceed not in ["yes", "y"]:
            return {"message": "Execution canceled by the user."}

        # Execute commands
        results = {}
        root_password = None

        for cmd in safe_commands:
            try:
                # Try executing the command
                print(f"\nExecuting: {cmd}")
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

                # Check if permission denied error occurs
                if "Permission denied" in result.stderr or result.returncode == 1:
                    print(f"Permission denied for command: {cmd}")
                    if root_password is None:
                        root_password = getpass("Enter root password for privileged commands: ")
                    # Re-execute with sudo
                    sudo_cmd = f"echo {root_password} | sudo -S {cmd}"
                    result = subprocess.run(sudo_cmd, shell=True, capture_output=True, text=True)

                results[cmd] = {
                    "status": "success" if result.returncode == 0 else "failed",
                    "output": result.stdout.strip(),
                    "error": result.stderr.strip(),
                }
                print(f"Result: {results[cmd]['status']}")
                if result.stderr.strip():
                    print(f"Error: {results[cmd]['error']}")
            except Exception as e:
                results[cmd] = {"status": "error", "error": str(e)}
                print(f"Error executing '{cmd}': {e}")

        return {
            "executed_commands": safe_commands,
            "skipped_commands": harmful_commands,
            "results": results,
        }

    @staticmethod
    def is_harmful_command(cmd: str) -> bool:
        """
        Determine if a command is harmful based on predefined criteria.

        Args:
            cmd (str): The command string to evaluate.

        Returns:
            bool: True if the command is harmful, otherwise False.
        """
        for excluded_cmd in CommandExecutionTool.EXCLUDED_COMMANDS:
            if excluded_cmd in cmd:
                return True
        return False

    @staticmethod
    def split_commands(commands: str) -> list:
        """
        Split a single command string with '&&' into individual commands.

        Args:
            commands (str): A single command string that contains multiple commands separated by '&&'.

        Returns:
            list: A list of individual commands.
        """
        # Split the string by '&&' and strip spaces from each command
        return [cmd.strip() for cmd in commands.split("&&")]

    def get_schema(self) -> dict:
        """
        Returns the JSON schema for the CommandExecutionTool's input parameters.

        Schema:
        - commands: A list of valid shell commands to execute sequentially.
        - confirm_harmful: A boolean indicating whether harmful commands flagged by the tool should be executed.

        Examples:
        Input:
        {
            "commands": [
                "mkdir ~/test",
                "touch ~/test/test.py"
            ],
            "confirm_harmful": false
        }
        """
        return {
            "type": "object",
            "properties": {
                "commands": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "A list of valid shell commands to execute sequentially. Examples: "
                        '"commands": ["mkdir ~/path/foldername", "touch ~/path/filename"]. '
                        "If a single string is provided, it will be split into individual commands using '&&'."
                    ),
                },
                "confirm_harmful": {
                    "type": "boolean",
                    "description": (
                        "Indicates whether flagged harmful commands should be executed. "
                        "If true, harmful commands will be executed; if false, they will be skipped."
                    ),
                },
            },
            "required": ["commands"],
        }