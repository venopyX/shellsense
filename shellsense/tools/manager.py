import requests
from shellsense.config.settings import Config
from shellsense.ai.prompts.instructions import tool_caller_ai, system_prompt
from shellsense.ai.providers.friendly_ai_response import FriendlyAiResponse
from shellsense.tools.data.stock import StockTool
from shellsense.tools.web.websearch import WebSearchTool
from shellsense.tools.web.crawler import CrawlerTool
from shellsense.tools.web.producthunt import ProductHuntTool
from shellsense.tools.media.screenshoter import ScreenshotTool
from shellsense.tools.language.translator import TranslatorTool
from shellsense.tools.data.wikipedia_search import WikipediaSearchTool
from shellsense.tools.coder import CoderTool
from shellsense.tools.data.github import GitHubTool
from shellsense.tools.shell.command_execution import CommandExecutionTool
from shellsense.utils.futuristic_loading import FuturisticLoading

loader = FuturisticLoading()

class ToolManager:
    def __init__(self):
        self.account_id = Config.ACCOUNT_ID
        self.api_token = Config.API_TOKEN
        self.url = Config.CLOUDFLARE_API_URL

        # Initialize available tools
        self.tool_mapping = self.load_tools()
        self.friendly_ai_response = FriendlyAiResponse()  # Create an instance of FriendlyAiResponse

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
            # "wikipediaSearch": WikipediaSearchTool(),
            "generateCode": CoderTool(),
        }

    def prepare_tools_schema(self):
        """
        Prepare the tools schema for Cloudflare Function Calling.
        """
        tools_schema = []
        for tool_name, tool_instance in self.tool_mapping.items():
            tools_schema.append({
                "name": tool_name,
                "description": tool_instance.__doc__,
                "parameters": tool_instance.get_schema()
            })
        # print(f"Prepared Tool Schemas: {tools_schema}")  # Debugging tool schema preparation
        return tools_schema

    def process_query(self, user_query):
        """
        Process the user query by calling Cloudflare's API and handle both tool calls and direct responses.
        """

        loader.start("Processing... ", "CYAN")

        # Generate available tool names dynamically
        tool_names = list(self.tool_mapping.keys())
        tool_names_str = f"Available tools: {tool_names}"
        # print(f"Tool Names: {tool_names_str}")

        payload = {
            "messages": [
            {"role": "system", "content": f"This is system instruction for you to guide you: {system_prompt()}"},
            {"role": "system", "content": tool_caller_ai(tool_names_str)},
            {"role": "user", "content": user_query}
            ],
            "tools": self.prepare_tools_schema(),
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_token}",
        }

        # print(f"Payload: {payload}")  # Debugging payload
        # print(f"Headers: {headers}")  # Debugging headers

        try:
            # Call Cloudflare API to determine response
            response = requests.post(self.url, json=payload, headers=headers)
            response.raise_for_status()
            # print(f"Cloudflare API Response: {response.text}")  # Debugging Cloudflare response

            data = response.json()
            result = data.get("result", {})

            # Handle tool calls if present
            tool_calls = result.get("tool_calls", [])
            if tool_calls:
                loader.text("Using tools...", "CYAN")
                # print(f"Tool Calls: {tool_calls}")  # Debugging tool calls
                aggregated_output = []
                for tool_call in tool_calls:
                    tool_name = tool_call.get("name")
                    arguments = tool_call.get("arguments", {})
                    # print(f"Processing tool call: {tool_name} with arguments: {arguments}")  # Debugging tool call processing

                    # Invoke the tool
                    raw_tool_output = self.call_tool(tool_name, arguments)
                    # print(f"Tool: {tool_name}, Raw Output: {raw_tool_output}")  # Debugging raw tool output
                    aggregated_output.append({
                        "tool": tool_name,
                        "output": raw_tool_output
                    })

                # Aggregate tool outputs into a single response
                combined_tool_output = "\n\n".join(
                    f"Tool: {item['tool']}\nOutput: {item['output']}" for item in aggregated_output
                )
                # print(f"Combined Tool Outputs: {combined_tool_output}")  # Debugging combined tool outputs

                # Use AI to refine the aggregated tool outputs for user-friendly response
                loader.text("Analysing...", "CYAN")
                friendly_response = self.friendly_ai_response.get_friendly_response(
                    user_query=user_query,
                    tool_output=combined_tool_output
                )
                # print(f"Friendly AI Response: {friendly_response}")  # Debugging AI refinement
                loader.stop("Completed! ", "GREEN")
                loader.clear()
                return friendly_response

            # Check for direct AI response
            ai_response = result.get("response", None)
            if ai_response:
                # print(f"Direct AI Response: {ai_response}")  # Debugging direct AI response
                loader.stop("Completed! ", "GREEN")
                loader.clear()
                return ai_response

            loader.text("No Response! ", "YELLOW")
            friendly_response = self.friendly_ai_response.get_friendly_response(
            user_query=user_query,
            tool_output=response.text
            )
            # print(f"Friendly AI Response: {friendly_response}")  # Debugging AI refinement
            loader.stop("Completed! ", "GREEN")
            loader.clear()
            return friendly_response

        except Exception as e:
            loader.stop("Failed! ", "RED")
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
        tool_instance = self.tool_mapping.get(tool_name)
        if tool_instance:
            try:
                result = tool_instance.invoke(arguments)
                # print(f"Tool: {tool_name}, Result: {result}")  # Debugging tool invocation result
                return result
            except Exception as e:
                print(f"Error invoking tool '{tool_name}': {e}")
                return {"error": f"Failed to invoke tool '{tool_name}': {str(e)}"}
        print(f"Tool '{tool_name}' not found.")
        return {"error": f"Tool '{tool_name}' not found."}
