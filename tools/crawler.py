# tools/crawler.py

from bs4 import BeautifulSoup
import requests
from tools.base_tool import BaseTool

class CrawlerTool(BaseTool):
    """
    Scrapes visible text and metadata from a specified webpage URL.
    """

    def invoke(self, input: dict) -> dict:
        url = input.get("url")
        if not url:
            return {"error": "URL parameter is required."}

        try:
            # Send a GET request to the URL
            response = requests.get(url)
            if response.status_code != 200:
                return {"error": f"Failed to retrieve content. Status code: {response.status_code}"}

            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            elements_with_text = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'b', 'strong', 'em']
            visible_texts = []

            # Extract visible text content
            for element in soup.find_all(elements_with_text):
                text_content = element.get_text(separator=' ', strip=True)
                if text_content:
                    visible_texts.append(f"{element.name}: {text_content}")

            result_text = ' '.join(visible_texts)
            return {"text": result_text[:10000]}  # Limiting text to 10,000 characters

        except Exception as e:
            return {"error": f"Exception during web scraping: {str(e)}"}

    def get_schema(self) -> dict:
        """
        Returns the JSON schema for the crawler tool's input parameters.
        """
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL of the webpage to scrape."
                }
            },
            "required": ["url"]
        }
