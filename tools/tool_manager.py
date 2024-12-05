import requests
from config.settings import Config
from pyplugin.utils.friendly_ai import FriendlyAiResponse
from tools.stock import StockTool
from tools.websearch import WebSearchTool
from tools.crawler import CrawlerTool
from tools.producthunt import ProductHuntTool
from tools.screenshoter import ScreenshotTool
from tools.translator import TranslatorTool
from tools.wikipedia_search import WikipediaSearchTool
from tools.coder import CoderTool
from tools.github import GitHubTool
from tools.generic_ai_response import GenericAiResponseTool
from tools.command_execution import CommandExecutionTool

class ToolManager:
    def __init__(self):
        self.account_id = Config.ACCOUNT_ID
        self.api_token = Config.API_TOKEN
        self.url = Config.CLOUDFLARE_API_URL

        # Initialize available tools
        self.tool_mapping = self.load_tools()

    def load_tools(self):
        """
        Load all available tools into the tool mapping.
        """
        return {
            "executeShellCommands": CommandExecutionTool(),
            "getGithubUserInfo": GitHubTool(),
            "getCurrentStockPrice": StockTool(),
            "performWebSearch": WebSearchTool(),
            "scrapeVisibleText": CrawlerTool(),
            "getProductHuntTrending": ProductHuntTool(),
            "takeScreenshotOfWebPage": ScreenshotTool(),
            "translateText": TranslatorTool(),
            "wikipediaSearch": WikipediaSearchTool(),
            "generateCode": CoderTool(),
            "genericAiResponse": GenericAiResponseTool(),
        }

    def prepare_tools_schema(self):
        """
        Prepare the tools schema for Cloudflare Function Calling.
        """
        tools_schema = []
        for tool_name, tool_instance in self.tool_mapping.items():
            schema = tool_instance.get_schema()
            tools_schema.append({
                "name": tool_name,
                "description": tool_instance.__doc__ or "No description provided.",
                "parameters": schema
            })
        # print(f"Prepared Tool Schemas: {tools_schema}")  # Debugging tool schema preparation
        return tools_schema

    def process_query(self, user_query):
        """
        Process the user query by calling Cloudflare's API and handle both tool calls and direct responses.
        """
        # Generate available tool names dynamically
        tool_names = list(self.tool_mapping.keys())
        tool_names_str = f"Available tools: {tool_names}"
        # print(tool_names_str)

        payload = {
            "messages": [
                {"role": "system", "content": f"You are shellsenseAI zsh assistant. Use the supplied tools to assist the user.\n\n{tool_names_str}. \n\nTo use executeShellCommands tool, you must convert user's query into valid shell commands/script! Don't use 'cd' command since you can't cd into other folder, execute command with path directly instead!"},
                {"role": "user", "content": user_query}
            ],
            "tools": self.prepare_tools_schema(),
            "strict": True,
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_token}",
        }
        try:
            # Call Cloudflare API to determine response
            response = requests.post(self.url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            result = data.get("result", {})
            # print(f"Cloudflare API Response: {response.text}")  # Debugging Cloudflare response

            # Handle tool calls if present
            tool_calls = result.get("tool_calls", [])
            if tool_calls:
                aggregated_output = []
                for tool_call in tool_calls:
                    tool_name = tool_call.get("name")
                    arguments = tool_call.get("arguments", {})

                    # Check for invalid or unmapped tool calls
                    if tool_name not in self.tool_mapping:
                        print(f"Invalid tool call: {tool_name}, Arguments: {arguments}")
                        aggregated_output.append({
                            "tool": tool_name,
                            "output": {"error": f"Tool '{tool_name}' is not available."}
                        })
                        continue

                    # Invoke the tool
                    raw_tool_output = self.call_tool(tool_name, arguments)
                    aggregated_output.append({
                        "tool": tool_name,
                        "output": raw_tool_output
                    })

                # Aggregate tool outputs into a single response
                combined_tool_output = "\n\n".join(
                    f"Tool: {item['tool']}\nOutput: {item['output']}" for item in aggregated_output
                )
                # print(f"Combined Tool Outputs: {combined_tool_output}")  # Debugging tool outputs

                # Use AI to refine the aggregated tool outputs for user-friendly response
                friendly_response = FriendlyAiResponse.get_friendly_response(
                    user_query=user_query,
                    tool_output=combined_tool_output
                )
                # print(f"Friendly AI Response: {friendly_response}")  # Debugging AI refinement
                return friendly_response

            # Check for direct AI response
            ai_response = result.get("response", None)
            if ai_response:
                # print(f"Direct AI Response: {ai_response}")  # Debugging direct AI response
                print({ai_response})
                return ai_response

            # Fallback if no response is generated
            print("No response from tools or AI.")
            return "I'm sorry, I couldn't process your query."

        except Exception as e:
            print(f"Error processing query: {str(e)}")
            return f"Error processing your query: {str(e)}"

    def call_tool(self, tool_name, arguments):
        """
        Invoke the corresponding tool function based on the tool name.

        Args:
            tool_name (str): Name of the tool to call.
            arguments (dict): Arguments to pass to the tool.

        Returns:
            dict: Result from the tool function.
        """
        # Map alternative names to canonical tool names
        # canonical_tool_name = {
        #     "githubSearchUser": "getGithubUserInfo",
        #     "githubUserSearch": "getGithubUserInfo"
        # }.get(tool_name, tool_name)  # Default to original name if not mapped.

        # tool_instance = self.tool_mapping.get(canonical_tool_name)
        tool_instance = self.tool_mapping.get(tool_name)
        if tool_instance:
            try:
                result = tool_instance.invoke(arguments)
                # print(f"Tool: {tool_name}, Result: {result}")  # Debugging tool invocation
                return result
            except Exception as e:
                print(f"Error invoking tool '{tool_name}': {e}")
                return {"error": f"Failed to invoke tool '{tool_name}': {str(e)}"}
        print(f"Tool '{tool_name}' not found.")
        return {"error": f"Tool '{tool_name}' not found."}
