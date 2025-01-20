from bs4 import BeautifulSoup
from requests_html import HTMLSession

from shellsense.tools.base_tool import BaseTool


class CrawlerTool(BaseTool):
    """
    Extracts visible text and metadata from a webpage.

    Args:
        url (str): The URL of the webpage to scrape (required, must start with 'http://' or 'https://').

    Parses the provided URL and extracts text from elements like paragraphs, headings, and emphasized text.
    The tool is ideal for summarizing webpage content or answering queries like "What does this URL contain?"
    The output is capped at 10,000 characters for readability.
    """

    def invoke(self, input: dict) -> dict:
        """
        Scrape and return visible text content from a webpage.

        Args:
            input (dict):
                url (str): The URL of the webpage to scrape (required).

        Returns:
            dict: Extracted text capped at 10,000 characters, or an error message.
        """
        url = input.get("url")
        if not url:
            return {"error": "URL parameter is required."}

        # Ensure the URL has a valid protocol (http/https)
        if not url.startswith(("http://", "https://")):
            if url.startswith(("www.", "://")):
                url = "https://" + url
            else:
                url = "https://" + url

        try:
            # Create an HTML session and render the page
            session = HTMLSession()
            response = session.get(url)
            print(f"Reading content from {url}... Please hold on for up to 60 seconds.")
            response.html.render(sleep=60)  # Wait for JavaScript content to load

            # Parse the rendered HTML content
            soup = BeautifulSoup(response.html.html, "html.parser")
            elements_with_text = [
                "p",
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "h6",
                "b",
                "strong",
                "em",
            ]
            visible_texts = []

            # Extract visible text content
            for element in soup.find_all(elements_with_text):
                text_content = element.get_text(separator=" ", strip=True)
                if text_content:
                    visible_texts.append(f"{element.name}: {text_content}")

            result_text = " ".join(visible_texts)
            return {"text": result_text[:10000]}  # Limiting text to 10,000 characters

        except Exception as e:
            return {"error": f"Exception during web scraping: {str(e)}"}

    def get_schema(self) -> dict:
        """
        Provide input parameter details for the tool.

        Returns:
            dict: JSON schema specifying the required 'url' parameter.
        """
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL of the webpage to scrape. Must start with 'http://' or 'https://'.",
                }
            },
            "required": ["url"],
        }
