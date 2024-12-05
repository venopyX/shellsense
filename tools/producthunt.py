# tools/producthunt.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tools.base_tool import BaseTool

class ProductHuntTool(BaseTool):
    """
    Fetches trending products from Product Hunt's daily leaderboard.
    """

    def invoke(self, input: dict) -> dict:
        url = "https://www.producthunt.com/leaderboard/daily/2024/11/7/all"
        try:
            response = requests.get(url)
            if response.status_code != 200:
                return {"error": f"Failed to retrieve Product Hunt data. Status code: {response.status_code}"}

            soup = BeautifulSoup(response.content, 'html.parser')
            products = soup.find_all('div', class_='styles_item__Dk_nz')
            trending_products = []

            # Extract product information
            for product in products[:5]:  # Limit to top 5 products
                title = product.find('strong').get_text(strip=True)
                votes = product.find('div', class_='styles_voteCountItem__zwuqk').get_text(strip=True)
                description_tag = product.find('a', class_='text-14')
                description = description_tag.get_text(strip=True) if description_tag else ""
                link = urljoin(url, product.find('a')['href'])
                image_tag = product.find('img')
                image = image_tag['src'] if image_tag else ""

                trending_products.append({
                    'title': title,
                    'votes': votes,
                    'description': description,
                    'link': link,
                    'image': image
                })

            return {"products": trending_products}
        except Exception as e:
            return {"error": f"Exception during Product Hunt data retrieval: {str(e)}"}

    def get_schema(self) -> dict:
        """
        Returns the JSON schema for the Product Hunt tool's input parameters.
        """
        return {
            "type": "object",
            "properties": {},
            "required": []
        }
