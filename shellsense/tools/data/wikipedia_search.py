# tools/wikipedia_search.py

import logging
from pydantic import BaseModel, Field
from wikipedia import page, search, PageError, DisambiguationError
from tools.base_tool import BaseTool

logger = logging.getLogger(__name__)

class WikipediaSearchTool(BaseTool):
    """
    Performs a Wikipedia search and returns the top result or related suggestions. 
    This tool allows users to quickly retrieve relevant Wikipedia pages based on a search query, 
    providing the page title, URL, and a summary. It also handles cases where no exact match is found 
    or when the query leads to multiple possible results.
    """

    def invoke(self, input: dict) -> dict:
        query = input.get("query")

        if not query:
            return {"error": "Query parameter is required."}

        try:
            # Attempt to fetch the Wikipedia page content and URL
            wiki_page = page(query)
            result = {
                "title": wiki_page.title,
                "url": wiki_page.url,
                "summary": wiki_page.summary,
            }

            return {"result": result}

        except PageError:
            # Page not found, suggest similar entries
            similar_results = search(query)
            logger.info(f"No exact match found for [{query}]. Suggestions: {similar_results}")
            return {"error": f"No exact match found. Similar results: {similar_results}"}

        except DisambiguationError as e:
            # Multiple possible results found
            logger.info(f"Disambiguation error for [{query}]. Suggestions: {e.options}")
            return {"error": f"Ambiguous query. Suggestions: {e.options}"}

        except Exception as e:
            logger.error(f"Error during Wikipedia search: {str(e)}")
            return {"error": f"Exception during Wikipedia search: {str(e)}"}

    def get_schema(self) -> dict:
        """
        Returns the JSON schema for the Wikipedia search tool's input parameters.
        """
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to look up on Wikipedia."
                }
            },
            "required": ["query"]
        }
