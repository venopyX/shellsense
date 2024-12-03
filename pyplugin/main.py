import os
import sys
from pathlib import Path

# Automatically detect the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pyplugin.utils.helper import OpenAIProvider, CloudflareProvider

def main():
    import argparse
    parser = argparse.ArgumentParser(description="ShellSense Plugin")
    parser.add_argument("-c", "--chat", type=str, help="Chat with OpenAI GPT model")
    parser.add_argument("-cf", "--cloudflare", type=str, help="Chat with Cloudflare Workers AI")
    args = parser.parse_args()

    if args.chat:
        provider = OpenAIProvider()
        response = provider.chat(args.chat)
        print(response)
    elif args.cloudflare:
        provider = CloudflareProvider()
        response = provider.chat(args.cloudflare)
        print(response)

if __name__ == "__main__":
    main()
