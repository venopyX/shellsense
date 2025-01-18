import logging
from typing import Dict, Any, List, Optional
import wikipedia
from shellsense.tools.base import BaseTool

logger = logging.getLogger(__name__)

class WikipediaSearchTool(BaseTool):
    """
    A tool for searching and retrieving information from Wikipedia.
    Supports searching articles, getting summaries, and retrieving full content.
    """

    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search Wikipedia and retrieve article information.

        Args:
            input_data (Dict[str, Any]): Input containing:
                - query (str): Search query
                - language (str, optional): Wikipedia language (default: en)
                - sentences (int, optional): Number of sentences in summary (default: 5)
                - full_content (bool, optional): Get full article content (default: False)

        Returns:
            Dict[str, Any]: Search results or error message

        Raises:
            ValueError: If query is missing or invalid
            wikipedia.exceptions.WikipediaException: If the search fails
        """
        try:
            self.validate_input(input_data)
            
            query = input_data["query"]
            language = input_data.get("language", "en")
            sentences = input_data.get("sentences", 5)
            full_content = input_data.get("full_content", False)
            
            # Set language
            wikipedia.set_lang(language)
            
            logger.info(f"Searching Wikipedia for: {query}")
            return self._search_wikipedia(query, sentences, full_content)
            
        except ValueError as e:
            logger.error(f"Invalid input: {str(e)}")
            return {"error": f"Invalid input: {str(e)}"}
        except wikipedia.exceptions.WikipediaException as e:
            logger.error(f"Wikipedia error: {str(e)}")
            return {"error": f"Wikipedia error: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {"error": f"Search failed: {str(e)}"}

    def _search_wikipedia(self, query: str, sentences: int, full_content: bool) -> Dict[str, Any]:
        """
        Perform Wikipedia search and get article content.

        Args:
            query (str): Search query
            sentences (int): Number of sentences in summary
            full_content (bool): Whether to get full article content

        Returns:
            Dict[str, Any]: Search results
        """
        try:
            # Search for articles
            search_results = wikipedia.search(query)
            if not search_results:
                logger.warning(f"No results found for: {query}")
                return {"error": "No results found"}
            
            # Get the first matching article
            page = wikipedia.page(search_results[0])
            
            result = {
                "title": page.title,
                "url": page.url,
                "summary": wikipedia.summary(search_results[0], sentences=sentences),
                "references": page.references[:10],  # Limit references
                "categories": page.categories[:10],  # Limit categories
                "related_titles": search_results[1:6]  # Include other search results
            }
            
            if full_content:
                result["content"] = page.content
                
            logger.debug(f"Successfully retrieved article: {page.title}")
            return result
            
        except wikipedia.exceptions.DisambiguationError as e:
            logger.info(f"Disambiguation page found for: {query}")
            return {
                "disambiguation": True,
                "options": e.options[:10],  # Limit disambiguation options
                "error": "Multiple matches found. Please be more specific."
            }
        except Exception as e:
            logger.error(f"Failed to retrieve article: {str(e)}")
            raise

    def get_schema(self) -> Dict[str, Any]:
        """
        Returns the JSON schema for the Wikipedia search tool's input parameters.

        Returns:
            Dict[str, Any]: JSON schema for validation and documentation.

        Example:
            {
                "query": "Python programming",
                "language": "en",
                "sentences": 5,
                "full_content": false
            }
        """
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query for Wikipedia"
                },
                "language": {
                    "type": "string",
                    "description": "Wikipedia language code (default: en)",
                    "pattern": "^[a-z]{2}(-[a-z]{2})?$"
                },
                "sentences": {
                    "type": "number",
                    "description": "Number of sentences in summary (default: 5)",
                    "minimum": 1,
                    "maximum": 10
                },
                "full_content": {
                    "type": "boolean",
                    "description": "Whether to retrieve full article content (default: false)"
                }
            },
            "required": ["query"]
        }
