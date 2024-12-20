from bs4 import BeautifulSoup
from requests_html import HTMLSession
from tools.base_tool import BaseTool

class CrawlerTool(BaseTool):
    """
    Scrapes visible text and metadata from a webpage. 
    This tool helps users understand the content of a webpage by extracting text from elements like paragraphs, 
    headings, and emphasized text. It is useful for queries like "What does this URL contain?" or "Summarize this webpage."
    By providing a URL, the tool parses the page and returns a summary of visible text. The output is concise, 
    informative, and capped at 10,000 characters for readability.
    """

    def invoke(self, input: dict) -> dict:
        url = input.get("url")
        if not url:
            return {"error": "URL parameter is required."}

        # Ensure the URL has a valid protocol (http/https)
        if not url.startswith(('http://', 'https://')):
            if url.startswith(('www.', '://')):
                url = 'https://' + url
            else:
                url = 'https://' + url

        try:
            # Create an HTML session and render the page
            session = HTMLSession()
            response = session.get(url)
            print(f"I'm Reading {url} contents... Please hold on just a minute(60 seconds)")
            response.html.render(sleep=60)  # Wait for 60 seconds for JS content to load

            # Parse the rendered HTML content
            soup = BeautifulSoup(response.html.html, 'html.parser')
            elements_with_text = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'b', 'strong', 'em']
            visible_texts = []

            # Extract visible text content
            for element in soup.find_all(elements_with_text):
                text_content = element.get_text(separator=' ', strip=True)
                if text_content:
                    visible_texts.append(f"{element.name}: {text_content}")

            result_text = ' '.join(visible_texts)
            # print(result_text)
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
                    "description": "The URL of the webpage to scrape. Ensure it starts with 'http://' or 'https://'."
                }
            },
            "required": ["url"]
        }