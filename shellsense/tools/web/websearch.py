import logging
import requests
from bs4 import BeautifulSoup
from typing import Dict, List
from urllib.parse import quote_plus
from googlesearch import SearchResult, search
from shellsense.tools.base_tool import BaseTool

logger = logging.getLogger(__name__)


class WebSearchTool(BaseTool):
    """
    Executes web searches and retrieves top results with titles, URLs, and descriptions.
    Useful for finding quick, relevant information on any topic.

    Args:
        query (str): The concised query string (required).
        num_results (int): Number of results to retrieve (default: 5).
    """

    def __init__(self):
        super().__init__()
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
        }

    def invoke(self, input: dict) -> dict:
        """
        Invoke the web search tool to perform searches on Google, Bing, and DuckDuckGo.

        Args:
            input (dict): Input parameters containing:
                - query (str): The search query to execute
                - num_results (int, optional): Number of results to return. Defaults to 5.

        Returns:
            dict: Search results containing titles, URLs, and descriptions

        Raises:
            ValueError: If query is not provided
        """
        query = input.get("query")
        num_results = input.get("num_results", 5)

        if not query:
            return {"error": "Query parameter is required."}

        try:
            google_results = self._google_search(query, num_results)
            bing_results = self._bing_search(query, num_results)
            ddg_results = self._ddg_search(query, num_results)

            # Combine all results
            combined_results = {
                "google": google_results,
                "bing": bing_results,
                "duckduckgo": ddg_results,
            }
            return {"results": combined_results}

        except Exception as e:
            logger.error(f"Error performing web search: {str(e)}")
            return {"error": f"Error performing web search: {str(e)}"}

    def _google_search(self, query: str, num_results: int) -> list:
        """Perform a Google search."""
        try:
            search_results = search(
                query, num_results=num_results, sleep_interval=2, advanced=True
            )
            return [
                {
                    "title": result.title or "No Title",
                    "url": result.url,
                    "description": result.description or "No Description",
                }
                for result in search_results
                if isinstance(result, SearchResult)
            ]
        except Exception as e:
            logger.error(f"Google search failed: {str(e)}")
            return []

    def _bing_search(self, query: str, num_results: int) -> List[Dict[str, str]]:
            """Perform Bing search."""
            results = []
            try:
                url = f"https://www.bing.com/search?q={quote_plus(query)}&count={num_results}"
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                search_results = soup.find_all('li', class_='b_algo')
                
                for result in search_results[:num_results]:
                    title_elem = result.find('h2')
                    link_elem = result.find('a')
                    snippet_elem = result.find('div', class_='b_caption')
                    
                    if title_elem and link_elem and snippet_elem:
                        results.append({
                            'title': title_elem.text.strip(),
                            'url': link_elem['href'],
                            'snippet': snippet_elem.text.strip()
                        })
                        
                return results
                
            except Exception as e:
                logger.error(f"Bing search failed: {str(e)}")
                return []

    def _ddg_search(self, query: str, num_results: int) -> list:
        """Perform a DuckDuckGo search."""
        try:
            url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            search_results = soup.find_all("div", class_="result")
            results = []
            for result in search_results[:num_results]:
                title_elem = result.find("a", class_="result__a")
                snippet_elem = result.find("a", class_="result__snippet")

                if title_elem and snippet_elem:
                    results.append(
                        {
                            "title": title_elem.text.strip(),
                            "url": title_elem["href"],
                            "description": snippet_elem.text.strip(),
                        }
                    )
            return results
        except Exception as e:
            logger.error(f"DuckDuckGo search failed: {str(e)}")
            return []

    def get_schema(self) -> dict:
        """
        Returns the JSON schema for the web search tool's input parameters.
        """
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to perform for up-to-date infos and future updates.",
                },
                "num_results": {
                    "type": "integer",
                    "description": (
                        "The number of search results to retrieve. Default: 5 and "
                        "use more than 5 if you need detailed info from many sources."
                    ),
                    "default": 5,
                },
            },
            "required": ["query"],
        }
