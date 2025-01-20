import argparse
import logging
from typing import Optional

from shellsense.ai.providers.cloudflare_provider import CloudflareProvider
from shellsense.ai.providers.openai_provider import OpenAIProvider
from shellsense.tools.tool_manager import ToolManager
from shellsense.utils.futuristic_loading import FuturisticLoading

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

loader = FuturisticLoading()


def process_chat(prompt: str, provider: str = "openai") -> Optional[str]:
    """
    Process a chat request using the specified AI provider.

    Args:
        prompt (str): The user's input prompt
        provider (str, optional): The AI provider to use. Defaults to "openai".

    Returns:
        Optional[str]: The AI's response or None if an error occurs
    """
    try:
        logger.info(f"Processing chat request with {provider} provider")
        if provider == "openai":
            ai_provider = OpenAIProvider()
            response = ai_provider.chat(prompt)
        else:  # cloudflare
            ai_provider = CloudflareProvider()
            response = ai_provider.chat([{"role": "user", "content": prompt}])
        logger.debug("Successfully processed chat request")
        return response
    except Exception as e:
        logger.error(f"Failed to process chat request: {str(e)}")
        return f"Error processing chat request: {str(e)}"


def process_tool_query(query: str) -> Optional[str]:
    """
    Process a query using the ToolManager.

    Args:
        query (str): The user's query to process

    Returns:
        Optional[str]: The processed response or None if an error occurs
    """
    try:
        logger.info("Processing tool query")
        tool_manager = ToolManager()
        loader.start("Processing query... ", "CYAN")
        response = tool_manager.process_query(query)
        loader.stop("Query completed! ", "GREEN")
        logger.debug("Successfully processed tool query")
        return response
    except Exception as e:
        logger.error(f"Failed to process tool query: {str(e)}")
        loader.stop("Query failed! ", "RED")
        return f"Error processing query: {str(e)}"


def main() -> None:
    """Main entry point for the ShellSense plugin."""
    try:
        parser = argparse.ArgumentParser(
            description="ShellSense - An intelligent shell assistant",
            epilog="For more information, visit: https://github.com/venopyX/shellsense",
        )
        parser.add_argument("-c", "--chat", type=str, help="Chat with OpenAI GPT model")
        parser.add_argument(
            "-cf", "--cloudflare", type=str, help="Chat with Cloudflare AI model"
        )
        parser.add_argument(
            "-q", "--query", type=str, help="Process a query with ShellSense tools"
        )
        args = parser.parse_args()

        if args.chat:
            response = process_chat(args.chat, "openai")
        elif args.cloudflare:
            response = process_chat(args.cloudflare, "cloudflare")
        elif args.query:
            response = process_tool_query(args.query)
        else:
            logger.warning("No valid argument provided")
            print("Error: No valid argument provided. Use -h or --help for usage.")
            return

        if response:
            print(response)

    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        print(f"An error occurred: {str(e)}")
        print("For help, use -h or --help")


if __name__ == "__main__":
    main()
