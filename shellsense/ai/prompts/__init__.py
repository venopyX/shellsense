"""
ShellSense AI prompts package.
"""

from .instructions import (coder_ai_prompt, friendly_ai, system_prompt,
                           tool_caller_ai)

__all__ = ["system_prompt", "coder_ai_prompt", "tool_caller_ai", "friendly_ai"]
