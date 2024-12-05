# tools/screenshoter.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from tools.base_tool import BaseTool
import time

class ScreenshotTool(BaseTool):
    """
    Captures a screenshot of a specified webpage URL.
    """

    def invoke(self, input: dict) -> dict:
        url = input.get("url")
        output_path = input.get("output_path", "screenshot.png")
        width = input.get("width", 1920)
        height = input.get("height", 1080)

        if not url:
            return {"error": "URL parameter is required."}

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
            return {"status": "success", "path": output_path}
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
                "output_path": {
                    "type": "string",
                    "description": "The file path where the screenshot will be saved. use name of website as file name",
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
