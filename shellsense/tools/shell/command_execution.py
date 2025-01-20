import os
import subprocess
from getpass import getpass

from shellsense.tools.base_tool import BaseTool


class CommandExecutionTool(BaseTool):
    """
    Executes shell commands, creates files/folders, and performs operations in the user's home directory.

    Args:
        commands (list[str] | str): A list of shell commands or a single string of commands separated by '&&'.
            Examples:
                ["mkdir ~/test", "touch ~/test/file.txt"]
                "mkdir ~/test && touch ~/test/file.txt"
        confirm_harmful (bool): Whether flagged harmful commands should be executed.

    Notes:
        - Commands like `rm -rf /`, `shutdown`, and other explicitly excluded commands will be flagged as harmful.
        - This tool cannot use 'cd' to change directories. All commands must be executed with full paths.

    Security:
        - The tool warns against executing harmful commands and allows users to skip them unless explicitly confirmed.
    """

    EXCLUDED_COMMANDS = [
        "rm -rf /",
        "shutdown",
        "reboot",
        "dd if=",
        "mkfs",
        "wget http://",
    ]

    def invoke(self, input_data: dict) -> dict:
        """
        Execute the provided commands sequentially.

        Args:
            input_data (dict): A dictionary with the following keys:
                - commands (list[str] | str): Shell commands to execute.
                - confirm_harmful (bool): Whether flagged harmful commands should be executed.

        Returns:
            dict: A summary of executed and skipped commands with their statuses.
        """
        commands = input_data.get("commands", [])
        confirm_harmful = input_data.get("confirm_harmful", False)

        # Convert commands to list if provided as a single string
        if isinstance(commands, str):
            commands = self.split_commands(commands)

        if not commands:
            return {"error": "No commands provided for execution."}

        harmful_commands = [cmd for cmd in commands if self.is_harmful_command(cmd)]
        safe_commands = [cmd for cmd in commands if cmd not in harmful_commands]

        # Warn and skip harmful commands unless confirmed
        if harmful_commands and not confirm_harmful:
            return {
                "error": "Harmful commands detected. Execution aborted.",
                "harmful_commands": harmful_commands,
            }

        results = {}
        root_password = None

        for cmd in safe_commands:
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

                # Handle permission errors
                if "Permission denied" in result.stderr or result.returncode == 1:
                    if root_password is None:
                        root_password = getpass(
                            "Enter root password for privileged commands: "
                        )
                    sudo_cmd = f"echo {root_password} | sudo -S {cmd}"
                    result = subprocess.run(
                        sudo_cmd, shell=True, capture_output=True, text=True
                    )

                results[cmd] = {
                    "status": "success" if result.returncode == 0 else "failed",
                    "output": result.stdout.strip(),
                    "error": result.stderr.strip(),
                }
            except Exception as e:
                results[cmd] = {"status": "error", "error": str(e)}

        return {
            "executed_commands": safe_commands,
            "skipped_commands": harmful_commands,
            "results": results,
        }

    @staticmethod
    def is_harmful_command(cmd: str) -> bool:
        """
        Check if a command is flagged as harmful.

        Args:
            cmd (str): The command to evaluate.

        Returns:
            bool: True if the command is harmful, otherwise False.
        """
        return any(
            excluded in cmd for excluded in CommandExecutionTool.EXCLUDED_COMMANDS
        )

    @staticmethod
    def split_commands(commands: str) -> list:
        """
        Split a string of commands separated by '&&' into a list of individual commands.

        Args:
            commands (str): Commands separated by '&&'.

        Returns:
            list[str]: A list of individual commands.
        """
        return [cmd.strip() for cmd in commands.split("&&")]

    def get_schema(self) -> dict:
        """
        Provide the input schema for the tool.

        Returns:
            dict: JSON schema following Cloudflare API requirements.
        """
        return {
            "type": "object",
            "properties": {
                "commands": {
                    "type": "string",
                    "description": (
                        "A list of shell commands or a single string of commands separated by '&&'. "
                        "Examples: ['mkdir ~/test', 'touch ~/test/file.txt'] or 'mkdir ~/test && touch ~/test/file.txt'."
                    ),
                    "minLength": 1,
                    "maxLength": 131072,
                },
                "confirm_harmful": {
                    "type": "boolean",
                    "description": "Whether flagged harmful commands should be executed.",
                    "default": False,
                },
            },
            "required": ["commands"],
        }
