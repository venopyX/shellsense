import logging

from pydantic import BaseModel, Field
from wikipedia import DisambiguationError, PageError, page, search

from shellsense.tools.base_tool import BaseTool

logger = logging.getLogger(__name__)


class WikipediaSearchTool(BaseTool):
    """
    Searches Wikipedia and returns the top result or related suggestions.

    Args:
        query (str): The search query to look up on Wikipedia.
    """

    def invoke(self, input: dict) -> dict:
        query = input.get("query")

        if not query:
            return {"error": "Query parameter is required."}

        try:
            wiki_page = page(query)
            result = {
                "title": wiki_page.title,
                "url": wiki_page.url,
                "summary": wiki_page.summary,
            }

            return {"result": result}

        except PageError:
            similar_results = search(query)
            logger.info(f"No exact match for [{query}]. Suggestions: {similar_results}")
            return {"error": f"No exact match. Suggestions: {similar_results}"}

        except DisambiguationError as e:
            logger.info(f"Disambiguation error for [{query}]. Suggestions: {e.options}")
            return {"error": f"Ambiguous query. Suggestions: {e.options}"}

        except Exception as e:
            logger.error(f"Error during search: {str(e)}")
            return {"error": f"Search exception: {str(e)}"}

    def get_schema(self) -> dict:
        """
        Provides the input schema for the Wikipedia search tool.

        Returns:
            dict: JSON schema for the search query parameter.
        """
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query for Wikipedia.",
                }
            },
            "required": ["query"],
        }
