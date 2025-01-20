import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from shellsense.tools.base_tool import BaseTool


class ScreenshotTool(BaseTool):
    """
    Captures a screenshot image of a specified webpage.

    Args:
        url (str): The URL of the webpage to capture. Must start with 'http://' or 'https://'.
        image_name (str): The name of the output image file (default: 'screenshot.png').
            Use the domain name as the file name, e.g., 'google.png' for 'https://google.com'.
        width (int): The width of the image (default: 1920).
        height (int): The height of the image (default: 1080).

    Notes:
        - Ensures the URL is properly formatted with the 'https://' prefix if missing.
        - Use only if requested by the user.
    """

    def invoke(self, input: dict) -> dict:
        """
        Captures a webpage screenshot and saves it as an image file.

        Args:
            input (dict): A dictionary with the following keys:
                - url (str): The URL of the webpage to capture.
                - image_name (str): The output image file name (default: 'screenshot.png').
                - width (int): Browser window width (default: 1920).
                - height (int): Browser window height (default: 1080).

        Returns:
            dict: A status dictionary containing:
                - 'status': 'success' if the screenshot is captured successfully.
                - 'message': Details of the successful operation.
                - 'error': Details of any exception encountered during execution.
        """
        url = input.get("url")
        output_path = input.get("image_name", "screenshot.png")
        width = input.get("width", 1920)
        height = input.get("height", 1080)

        if not url:
            return {"error": "URL parameter is required."}

        # Add 'https://' if the URL doesn't start with a valid protocol
        if not url.startswith(("http://", "https://")):
            url = (
                f"https://{url.lstrip('://')}"
                if url.startswith(("www.", "://"))
                else f"https://{url}"
            )

        try:
            # Configure headless Chrome options
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument(f"--window-size={width},{height}")

            # Launch WebDriver and capture screenshot
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            time.sleep(2)  # Wait for page content to load
            driver.save_screenshot(output_path)
            driver.quit()

            # Verify screenshot integrity
            image = Image.open(output_path)
            image.verify()
            return {
                "status": "success",
                "message": f"Screenshot saved as '{output_path}'",
            }
        except Exception as e:
            return {"error": f"Exception during screenshot capture: {str(e)}"}

    def get_schema(self) -> dict:
        """
        Provides the input schema for the screenshot tool.

        Returns:
            dict: JSON schema specifying required and optional parameters.
        """
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL of the webpage to capture. Must start with 'http://' or 'https://'.",
                },
                "image_name": {
                    "type": "string",
                    "description": (
                        "The name of the output image file. Use the website name as the file name, "
                        "e.g., 'google.png' for 'https://google.com'."
                    ),
                    "default": "screenshot.png",
                },
                "width": {
                    "type": "integer",
                    "description": "The width of the browser window (default: 1920).",
                    "default": 1920,
                },
                "height": {
                    "type": "integer",
                    "description": "The height of the browser window (default: 1080).",
                    "default": 1080,
                },
            },
            "required": ["url"],
        }
