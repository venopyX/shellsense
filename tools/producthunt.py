# tools/producthunt.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from tools.base_tool import BaseTool

class ProductHuntTool(BaseTool):
    """
    Retrieves the top trending products from Product Hunt's daily leaderboard.
    This tool allows users to discover popular products by fetching the latest trending items on Product Hunt.
    You can specify a date or use the current day's leaderboard to get the top 5 products, including their title,
    vote count, description, link, and image. It is perfect for users looking to stay updated on the latest trends
    in tech, apps, and other products. e.g. "Today's producthunt products", "Producthunt leaderboard", "Best products of the day" etc
    """

    def invoke(self, input: dict) -> dict:
        # Get the date from input or use today's date
        date_str = input.get('date', datetime.today().strftime('%Y/%m/%d'))
        if date_str == "today":
            date_str = datetime.today().strftime('%Y/%m/%d')

        url = f"https://www.producthunt.com/leaderboard/daily/{date_str}/all"

        try:
            response = requests.get(url)
            if response.status_code != 200:
                return {"error": f"Failed to retrieve Product Hunt data. Status code: {response.status_code}"}

            soup = BeautifulSoup(response.content, 'html.parser')
            products = soup.find_all('section', class_='group')
            trending_products = []

            # Extract product information
            for product in products[:5]:  # Limit to top 5 products
                title_tag = product.find('a', class_='text-16')
                title = title_tag.get_text(strip=True) if title_tag else ""

                vote_button = product.find('button', class_='styles_reset__0clCw')
                votes = vote_button.get_text(strip=True) if vote_button else ""

                description_tag = product.find_all('a', class_='text-16')
                description = description_tag[1].get_text(strip=True) if len(description_tag) > 1 else ""

                link_tag = product.find('a', href=True)
                link = urljoin(url, link_tag['href']) if link_tag else ""

                image_tag = product.find('img') if not product.find('video') else product.find('video')
                image = image_tag['src'] if image_tag and image_tag.name == 'img' else (image_tag['poster'] if image_tag else "")

                trending_products.append({
                    'title': title,
                    'votes': votes,
                    'description': description,
                    'link': link,
                    'image': image
                })

            print(f"Products: {trending_products}")
            if trending_products == []:
                return "No product posts for this date."
            return {"products": trending_products}
        except Exception as e:
            print(f"Exception during Product Hunt data retrieval: {str(e)}")
            return {"error": f"Exception during Product Hunt data retrieval: {str(e)}"}

    def get_schema(self) -> dict:
        """
        Returns the JSON schema for the Product Hunt tool's input parameters.
        """
        return {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "format": "date",
                    "description": "The date for which to retrieve the trending products in YYYY/MM/DD format."
                }
            },
            "required": []
        }
