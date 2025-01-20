#!/usr/bin/env python3
"""
ShellSense - AI-powered terminal assistant
"""

import argparse
import logging
import os
import sys
from typing import Dict, Optional

from shellsense.config import create_default_config, load_config
from shellsense.tools.tool_manager import ToolManager

logger = logging.getLogger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="ShellSense - AI-powered terminal assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-p",
        "--provider",
        help="AI provider to use (cloudflare, openai, or gemini)",
        type=str,
        choices=["cloudflare", "openai", "gemini"],
        default="cloudflare",
    )

    parser.add_argument(
        "-q",
        "--query",
        help="Query to process",
        type=str,
        metavar="QUERY",
    )

    parser.add_argument(
        "--setup", help="Configure ShellSense settings", action="store_true"
    )

    return parser


def setup_shellsense() -> None:
    """Configure ShellSense settings."""
    try:
        create_default_config()
        print("Please edit the configuration file with your API keys.")
    except Exception as e:
        print(f"Error setting up ShellSense: {str(e)}")
        sys.exit(1)


def main(args: Optional[list[str]] = None) -> int:
    """Main entry point for ShellSense."""
    try:
        parser = create_parser()
        parsed_args = parser.parse_args(args)

        if parsed_args.setup:
            setup_shellsense()
            return 0

        # Load configuration
        try:
            config = load_config()
        except EnvironmentError as e:
            print(f"Error: {str(e)}")
            return 1

        # Initialize components
        try:
            tool_manager = ToolManager(provider=parsed_args.provider)

            # Handle commands
            if parsed_args.query:
                result = tool_manager.process_query(parsed_args.query)
                print(result)
            else:
                parser.print_help()
                return 1

            return 0

        except Exception as e:
            logger.error(f"Error: {str(e)}", exc_info=True)
            print(f"Error: {str(e)}")
            return 1

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        print(f"Unexpected error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
