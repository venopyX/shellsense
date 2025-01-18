import os
import logging
import subprocess
from typing import List, Union, Dict, Any
from getpass import getpass
from shellsense.tools.base import BaseTool

logger = logging.getLogger(__name__)

class CommandExecutionTool(BaseTool):
    """
    A tool to execute shell commands, create files/folders, and handle operations in the user's home directory.
    Use this tool, if user needs to know about their computer or wants you to interact with the computer!

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

    def invoke(self, input_data: dict) -> Dict[str, Any]:
        """
        Execute commands or create files/folders as per user input.

        Args:
            input_data (dict): Dictionary with the following keys:
                - commands (list or string): List of commands to execute (strings), or a single string with commands.
                - confirm_harmful (bool): True if commands are marked as harmful by AI.

        Returns:
            Dict[str, Any]: Status of the executed commands, including any errors or skipped commands.

        Raises:
            ValueError: If input commands are invalid or potentially harmful.
            subprocess.SubprocessError: If command execution fails.
        """
        try:
            logger.info("Processing command execution request")
            commands = input_data.get("commands", [])
            confirm_harmful = input_data.get("confirm_harmful", False)

            # Convert string commands to list
            if isinstance(commands, str):
                commands = self.split_commands(commands)

            # Validate commands
            if not commands:
                logger.error("No commands provided")
                return {"error": "No commands provided"}

            # Check for harmful commands
            harmful_commands = self.check_harmful_commands(commands)
            if harmful_commands and not confirm_harmful:
                logger.warning(f"Potentially harmful commands detected: {harmful_commands}")
                return {
                    "error": "Potentially harmful commands detected",
                    "harmful_commands": harmful_commands
                }

            # Execute commands
            results = []
            for cmd in commands:
                try:
                    logger.info(f"Executing command: {cmd}")
                    result = subprocess.run(
                        cmd,
                        shell=True,
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    results.append({
                        "command": cmd,
                        "output": result.stdout,
                        "status": "success"
                    })
                    logger.debug(f"Command executed successfully: {cmd}")
                except subprocess.SubprocessError as e:
                    logger.error(f"Command execution failed: {cmd}, Error: {str(e)}")
                    results.append({
                        "command": cmd,
                        "error": str(e),
                        "status": "failed"
                    })

            return {"results": results}

        except Exception as e:
            logger.error(f"Unexpected error in command execution: {str(e)}")
            return {"error": f"Command execution failed: {str(e)}"}

    def split_commands(self, commands_str: str) -> List[str]:
        """
        Split a string of commands into a list.

        Args:
            commands_str (str): String containing commands separated by '&&'.

        Returns:
            List[str]: List of individual commands.
        """
        try:
            return [cmd.strip() for cmd in commands_str.split("&&") if cmd.strip()]
        except Exception as e:
            logger.error(f"Failed to split commands: {str(e)}")
            return []

    def check_harmful_commands(self, commands: List[str]) -> List[str]:
        """
        Check for potentially harmful commands.

        Args:
            commands (List[str]): List of commands to check.

        Returns:
            List[str]: List of detected harmful commands.
        """
        try:
            harmful = []
            for cmd in commands:
                if any(excluded in cmd.lower() for excluded in self.EXCLUDED_COMMANDS):
                    harmful.append(cmd)
            return harmful
        except Exception as e:
            logger.error(f"Failed to check harmful commands: {str(e)}")
            return commands  # Return all commands as harmful if check fails

    def get_schema(self) -> dict:
        """
        Returns the JSON schema for the CommandExecutionTool's input parameters.

        Returns:
            dict: JSON schema for validation and documentation.
        """
        return {
            "type": "object",
            "properties": {
                "commands": {
                    "oneOf": [
                        {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of shell commands to execute"
                        },
                        {
                            "type": "string",
                            "description": "Single command or commands separated by '&&'"
                        }
                    ]
                },
                "confirm_harmful": {
                    "type": "boolean",
                    "description": "Whether to execute commands flagged as harmful"
                }
            },
            "required": ["commands"]
        }