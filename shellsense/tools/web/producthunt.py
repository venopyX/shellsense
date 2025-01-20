from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from shellsense.tools.base_tool import BaseTool


class ProductHuntTool(BaseTool):
    """
    Retrieves the top trending products from Product Hunt's daily leaderboard.

    Args:
        date (str, optional): The date to fetch products for, in YYYY/MM/DD format.
                              Defaults to today's date if not provided.

    Fetches the top 5 products from the specified date's leaderboard, including title, votes,
    description, link, and image. Ideal for discovering new and trending tech, apps, and products.
    """

    def invoke(self, input: dict) -> dict:
        """
        Retrieve top trending products from Product Hunt.

        Args:
            input (dict):
                date (str, optional): Date in YYYY/MM/DD format (defaults to today's date).

        Returns:
            dict: A list of top 5 trending products with details or an error message.
        """
        # Get the date from input or use today's date
        date_str = input.get("date", datetime.today().strftime("%Y/%m/%d"))
        if date_str == "today":
            date_str = datetime.today().strftime("%Y/%m/%d")

        url = f"https://www.producthunt.com/leaderboard/daily/{date_str}/all"

        try:
            response = requests.get(url)
            if response.status_code != 200:
                return {
                    "error": f"Failed to retrieve Product Hunt data. Status code: {response.status_code}"
                }

            soup = BeautifulSoup(response.content, "html.parser")
            products = soup.find_all("section", class_="group")
            trending_products = []

            # Extract product information
            for product in products[:5]:  # Limit to top 5 products
                title_tag = product.find("a", class_="text-16")
                title = title_tag.get_text(strip=True) if title_tag else ""

                vote_button = product.find("button", class_="styles_reset__0clCw")
                votes = vote_button.get_text(strip=True) if vote_button else ""

                description_tag = product.find_all("a", class_="text-16")
                description = (
                    description_tag[1].get_text(strip=True)
                    if len(description_tag) > 1
                    else ""
                )

                link_tag = product.find("a", href=True)
                link = urljoin(url, link_tag["href"]) if link_tag else ""

                image_tag = (
                    product.find("img")
                    if not product.find("video")
                    else product.find("video")
                )
                image = (
                    image_tag["src"]
                    if image_tag and image_tag.name == "img"
                    else (image_tag["poster"] if image_tag else "")
                )

                trending_products.append(
                    {
                        "title": title,
                        "votes": votes,
                        "description": description,
                        "link": link,
                        "image": image,
                    }
                )

            if not trending_products:
                return {"error": "No products found for the specified date."}
            return {"products": trending_products}

        except Exception as e:
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
                    "description": "Date to fetch products for in YYYY/MM/DD format. Defaults to today's date.",
                }
            },
            "required": [],
        }
