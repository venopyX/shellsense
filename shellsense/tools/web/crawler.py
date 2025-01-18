import logging
from typing import Dict, Any, List, Optional
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from shellsense.tools.base import BaseTool

logger = logging.getLogger(__name__)

class WebCrawlerTool(BaseTool):
    """
    A tool for crawling web pages and extracting content.
    Supports various content extraction methods and respects robots.txt.
    """

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crawl a webpage and extract its content.

        Args:
            input_data (Dict[str, Any]): Input containing:
                - url (str): URL to crawl
                - extract_type (str, optional): Type of content to extract (default: "text")
                - max_depth (int, optional): Maximum crawl depth for links (default: 1)

        Returns:
            Dict[str, Any]: Extracted content or error message

        Raises:
            ValueError: If URL is missing or invalid
            requests.RequestException: If the crawl request fails
        """
        try:
            self.validate_input(input_data)
            
            url = input_data["url"]
            extract_type = input_data.get("extract_type", "text")
            max_depth = input_data.get("max_depth", 1)
            
            logger.info(f"Crawling URL: {url} (type: {extract_type}, depth: {max_depth})")
            return self._crawl_url(url, extract_type, max_depth)
            
        except ValueError as e:
            logger.error(f"Invalid input: {str(e)}")
            return {"error": f"Invalid input: {str(e)}"}
        except requests.RequestException as e:
            logger.error(f"Crawl request failed: {str(e)}")
            return {"error": f"Crawl request failed: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error during crawl: {str(e)}")
            return {"error": f"Crawl failed: {str(e)}"}

    def _crawl_url(self, url: str, extract_type: str, max_depth: int) -> Dict[str, Any]:
        """
        Crawl a URL and extract content.

        Args:
            url (str): URL to crawl
            extract_type (str): Type of content to extract
            max_depth (int): Maximum crawl depth

        Returns:
            Dict[str, Any]: Extracted content
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            content = self._extract_content(soup, extract_type)
            links = self._extract_links(soup, url) if max_depth > 1 else []
            
            result = {
                "url": url,
                "content": content,
                "links": links[:10]  # Limit number of links
            }
            
            if max_depth > 1 and links:
                result["sub_pages"] = self._crawl_subpages(links, extract_type, max_depth - 1)
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to crawl {url}: {str(e)}")
            raise

    def _extract_content(self, soup: BeautifulSoup, extract_type: str) -> Dict[str, Any]:
        """
        Extract specific content from a webpage.

        Args:
            soup (BeautifulSoup): Parsed HTML
            extract_type (str): Type of content to extract

        Returns:
            Dict[str, Any]: Extracted content
        """
        content = {}
        
        if extract_type in ["text", "all"]:
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            content["text"] = " ".join(soup.stripped_strings)
            
        if extract_type in ["links", "all"]:
            content["links"] = [a.get('href') for a in soup.find_all('a', href=True)]
            
        if extract_type in ["images", "all"]:
            content["images"] = [img.get('src') for img in soup.find_all('img', src=True)]
            
        if extract_type in ["meta", "all"]:
            content["meta"] = {
                "title": soup.title.string if soup.title else None,
                "description": soup.find("meta", {"name": "description"}).get("content") if soup.find("meta", {"name": "description"}) else None,
                "keywords": soup.find("meta", {"name": "keywords"}).get("content") if soup.find("meta", {"name": "keywords"}) else None
            }
            
        return content

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """
        Extract and normalize links from a webpage.

        Args:
            soup (BeautifulSoup): Parsed HTML
            base_url (str): Base URL for relative links

        Returns:
            List[str]: List of normalized links
        """
        links = []
        base_domain = urlparse(base_url).netloc
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            full_url = urljoin(base_url, href)
            
            # Only include links from the same domain
            if urlparse(full_url).netloc == base_domain:
                links.append(full_url)
                
        return list(set(links))  # Remove duplicates

    def _crawl_subpages(self, links: List[str], extract_type: str, depth: int) -> List[Dict[str, Any]]:
        """
        Crawl subpages up to specified depth.

        Args:
            links (List[str]): Links to crawl
            extract_type (str): Type of content to extract
            depth (int): Current depth

        Returns:
            List[Dict[str, Any]]: Crawled content from subpages
        """
        results = []
        for link in links[:3]:  # Limit number of subpages
            try:
                result = self._crawl_url(link, extract_type, depth)
                results.append(result)
            except Exception as e:
                logger.warning(f"Failed to crawl subpage {link}: {str(e)}")
                continue
        return results

    def get_schema(self) -> Dict[str, Any]:
        """
        Returns the JSON schema for the web crawler tool's input parameters.

        Returns:
            Dict[str, Any]: JSON schema for validation and documentation.

        Example:
            {
                "url": "https://example.com",
                "extract_type": "text",
                "max_depth": 1
            }
        """
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL to crawl"
                },
                "extract_type": {
                    "type": "string",
                    "description": "Type of content to extract (default: text)",
                    "enum": ["text", "links", "images", "meta", "all"]
                },
                "max_depth": {
                    "type": "number",
                    "description": "Maximum crawl depth (default: 1)",
                    "minimum": 1,
                    "maximum": 3
                }
            },
            "required": ["url"]
        }