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
from shellsense.utils.loading import FuturisticLoading
from shellsense.utils.logging_manager import get_logger, log_function_call

# Initialize logger for this module
logger = get_logger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    logger.debug("Creating argument parser")
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

    logger.debug("Argument parser created successfully")
    return parser


def setup_shellsense() -> None:
    """Configure ShellSense settings."""
    logger.info("Starting ShellSense setup")
    try:
        create_default_config()
        logger.info("Default configuration created successfully")
        print("Please edit the configuration file with your API keys.")
    except Exception as e:
        logger.error("Failed to setup ShellSense", exc_info=True)
        print(f"Error setting up ShellSense: {str(e)}")
        sys.exit(1)


@log_function_call
def main(args: Optional[list[str]] = None) -> int:
    """Main entry point for ShellSense."""
    loading = FuturisticLoading()
    try:
        logger.info("Starting ShellSense")
        parser = create_parser()
        parsed_args = parser.parse_args(args)
        logger.debug("Command line arguments parsed", 
                    extra={"cli_args": vars(parsed_args)})

        if parsed_args.setup:
            setup_shellsense()
            return 0

        # Load configuration
        try:
            loading.start("Loading config...", "CYAN")
            logger.debug("Loading configuration")
            config = load_config()
            loading.text("Config loaded....", "GREEN")
            logger.info("Configuration loaded successfully")
        except EnvironmentError as e:
            loading.stop("Config error...", "RED")
            logger.error("Failed to load configuration", exc_info=True)
            print(f"Error: {str(e)}")
            return 1

        # Initialize components
        try:
            loading.text("Starting AI.....", "CYAN")
            logger.debug(f"Initializing ToolManager with provider: {parsed_args.provider}")
            tool_manager = ToolManager(provider=parsed_args.provider)
            loading.text("AI ready......", "GREEN")
            logger.info("ToolManager initialized successfully")

            # Handle commands
            if parsed_args.query:
                loading.text("Processing......", "CYAN")
                logger.info(f"Processing query: {parsed_args.query}")
                
                loading.text("Thinking.....", "MAGENTA")
                result = tool_manager.process_query(parsed_args.query)
                
                loading.text("Responding......", "BLUE")
                logger.debug("Query processed successfully", 
                           extra={"result": result})
                
                loading.stop("Response....:", "GREEN")
                print(result)
            else:
                loading.stop()
                logger.warning("No query provided, showing help message")
                parser.print_help()
                return 1

            logger.info("ShellSense completed successfully")
            return 0

        except Exception as e:
            loading.stop("Error...", "RED")
            logger.error("Error during tool execution", exc_info=True)
            print(f"Error: {str(e)}")
            return 1

    except Exception as e:
        if loading:
            loading.stop("Error...", "RED")
        logger.critical("Unexpected error occurred", exc_info=True)
        print(f"Unexpected error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
