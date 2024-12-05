import os
import sys
from pathlib import Path
import argparse

from pathlib import Path

# Automatically detect the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
    
from pyplugin.utils.helper import OpenAIProvider, CloudflareProvider
from tools.tool_manager import ToolManager
from config.settings import Config

# Automatically detect the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

def main():
    parser = argparse.ArgumentParser(description="ShellSense Plugin")
    parser.add_argument("-c", "--chat", type=str, help="Chat with OpenAI GPT model")
    parser.add_argument("-cf", "--cloudflare", type=str, help="Chat with Cloudflare Workers AI")
    parser.add_argument("-q", "--query", type=str, help="Process a query with CopiloHero tools")
    args = parser.parse_args()

    if args.chat:
        provider = OpenAIProvider()
        response = provider.chat(args.chat)
        print(response)
    elif args.cloudflare:
        provider = CloudflareProvider()
        response = provider.chat(args.cloudflare)
        print(response)
    elif args.query:
        tool_manager = ToolManager()
        print("Processing your query with Cloudflare AI Function Calling...")
        tool_manager.process_query(args.query)
    else:
        print("Error: No valid argument provided. Use -h or --help for usage.")


if __name__ == "__main__":
    Config.validate()  # Ensure configuration is loaded properly
    main()
