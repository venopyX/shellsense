import sys
import os

# Add the base directory to sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)

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
