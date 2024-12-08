# tools/screenshoter.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from tools.base_tool import BaseTool
import time

class ScreenshotTool(BaseTool):
    """
    Captures a screenshot of a given webpage URL using headless Chrome. 
    Allows specifying the image file name (default: "screenshot.png")
    use website name as image name. e.g. google.png for https://google.com
    and browser window dimensions (default: 1920x1080) as width and height. 
    The image is saved locally and verified for integrity.
    """

    def invoke(self, input: dict) -> dict:
        url = input.get("url")
        output_path = input.get("image_name", "screenshot.png")
        width = input.get("width", 1920)
        height = input.get("height", 1080)

        if not url:
            return {"error": "URL parameter is required."}

        # Ensure the URL has a valid protocol (http/https)
        if not url.startswith(('http://', 'https://')):
            if url.startswith(('www.', '://')):
                url = 'https://' + url
            else:
                url = 'https://' + url

        try:
            # Setup headless Chrome options
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument(f"--window-size={width},{height}")

            # Initialize WebDriver
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            time.sleep(2)  # Wait for page load

            # Capture screenshot
            driver.save_screenshot(output_path)
            driver.quit()

            # Confirm screenshot creation
            image = Image.open(output_path)
            image.verify()
            return {"status": "success", "message": f"Screenshot successfully taken and saved as {output_path}"}
        except Exception as e:
            return {"error": f"Exception during screenshot capture: {str(e)}"}

    def get_schema(self) -> dict:
        """
        Returns the JSON schema for the screenshot tool's input parameters.
        """
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL of the webpage to capture(start with http:// or https://)."
                },
                "image_name": {
                    "type": "string",
                    "description": "The image file name or path of the screenshot. use name of website as file name",
                    "default": "screenshot.png"
                },
                "width": {
                    "type": "integer",
                    "description": "The width of the browser window for capturing the screenshot.",
                    "default": 1920
                },
                "height": {
                    "type": "integer",
                    "description": "The height of the browser window for capturing the screenshot.",
                    "default": 1080
                }
            },
            "required": ["url"]
        }
