import argparse
from providers.cloudflare_provider import CloudflareProvider
from providers.openai_provider import OpenAIProvider
from tools.tool_manager import ToolManager

def main():
    parser = argparse.ArgumentParser(description="ShellSense Plugin")
    parser.add_argument("-c", "--chat", type=str, help="Chat with OpenAI GPT model")
    parser.add_argument("-cf", "--cloudflare", type=str, help="Chat with Cloudflare AI model")
    parser.add_argument("-q", "--query", type=str, help="Process a query with CopiloHero tools")
    args = parser.parse_args()

    if args.chat:
        provider = OpenAIProvider()
        response = provider.chat(args.chat)
        print(response)
    elif args.cloudflare:
        provider = CloudflareProvider()
        response = provider.chat([{"role": "user", "content": args.cloudflare}])
        print(response)
    elif args.query:
        tool_manager = ToolManager()
        print("Processing your query; this may take a moment...")
        response = tool_manager.process_query(args.query)
        print(response)
    else:
        print("Error: No valid argument provided. Use -h or --help for usage.")

if __name__ == "__main__":
    main()
