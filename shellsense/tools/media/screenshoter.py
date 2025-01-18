import logging
import os
from typing import Dict, Any, Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from shellsense.tools.base import BaseTool

logger = logging.getLogger(__name__)

class ScreenshotTool(BaseTool):
    """
    A tool for taking screenshots of web pages using Selenium.
    Supports various screenshot options and viewport sizes.
    """

    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--window-size=1920,1080')

    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Take a screenshot of a webpage.

        Args:
            input_data (Dict[str, Any]): Input containing:
                - url (str): URL to screenshot
                - output_path (str): Path to save the screenshot
                - wait_time (int, optional): Time to wait for page load (default: 5)
                - full_page (bool, optional): Capture full page (default: False)

        Returns:
            Dict[str, Any]: Screenshot info or error message

        Raises:
            ValueError: If URL or output path is missing or invalid
            WebDriverException: If browser automation fails
        """
        try:
            self.validate_input(input_data)
            
            url = input_data["url"]
            output_path = input_data["output_path"]
            wait_time = input_data.get("wait_time", 5)
            full_page = input_data.get("full_page", False)
            
            logger.info(f"Taking screenshot of URL: {url}")
            return self._take_screenshot(url, output_path, wait_time, full_page)
            
        except ValueError as e:
            logger.error(f"Invalid input: {str(e)}")
            return {"error": f"Invalid input: {str(e)}"}
        except WebDriverException as e:
            logger.error(f"Browser automation failed: {str(e)}")
            return {"error": f"Screenshot failed: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error during screenshot: {str(e)}")
            return {"error": f"Screenshot failed: {str(e)}"}

    def _take_screenshot(self, url: str, output_path: str, wait_time: int, full_page: bool) -> Dict[str, Any]:
        """
        Take the actual screenshot using Selenium.

        Args:
            url (str): URL to screenshot
            output_path (str): Path to save the screenshot
            wait_time (int): Time to wait for page load
            full_page (bool): Capture full page

        Returns:
            Dict[str, Any]: Screenshot info
        """
        driver = None
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Initialize webdriver
            driver = webdriver.Chrome(options=self.chrome_options)
            driver.get(url)
            
            # Wait for page load
            try:
                WebDriverWait(driver, wait_time).until(
                    EC.presence_of_element_located(("tag name", "body"))
                )
            except TimeoutException:
                logger.warning(f"Page load timeout after {wait_time} seconds")
            
            if full_page:
                # Get scroll height
                total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
                driver.set_window_size(1920, total_height)
            
            # Take screenshot
            driver.save_screenshot(output_path)
            
            # Get page info
            title = driver.title
            current_url = driver.current_url
            
            logger.info(f"Screenshot saved to: {output_path}")
            return {
                "success": True,
                "file_path": output_path,
                "page_title": title,
                "final_url": current_url,
                "full_page": full_page
            }
            
        except Exception as e:
            logger.error(f"Failed to take screenshot: {str(e)}")
            raise
            
        finally:
            if driver:
                try:
                    driver.quit()
                except Exception as e:
                    logger.warning(f"Failed to close browser: {str(e)}")

    def get_schema(self) -> Dict[str, Any]:
        """
        Returns the JSON schema for the screenshot tool's input parameters.

        Returns:
            Dict[str, Any]: JSON schema for validation and documentation.

        Example:
            {
                "url": "https://example.com",
                "output_path": "/path/to/screenshot.png",
                "wait_time": 5,
                "full_page": false
            }
        """
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL to take screenshot of"
                },
                "output_path": {
                    "type": "string",
                    "description": "Path to save the screenshot (PNG format)"
                },
                "wait_time": {
                    "type": "number",
                    "description": "Time to wait for page load in seconds (default: 5)",
                    "minimum": 1,
                    "maximum": 30
                },
                "full_page": {
                    "type": "boolean",
                    "description": "Whether to capture the full page (default: false)"
                }
            },
            "required": ["url", "output_path"]
        }

    def validate_input(self, input_data: Dict[str, Any]) -> None:
        """
        Validate the input data for the screenshot tool.

        Args:
            input_data (Dict[str, Any]): Input data to validate

        Raises:
            ValueError: If input data is invalid
        """
        if not isinstance(input_data, dict):
            raise ValueError("Input data must be a dictionary")

        required_keys = ["url", "output_path"]
        for key in required_keys:
            if key not in input_data:
                raise ValueError(f"Missing required key: {key}")

        if not isinstance(input_data["url"], str):
            raise ValueError("URL must be a string")

        if not isinstance(input_data["output_path"], str):
            raise ValueError("Output path must be a string")

        if "wait_time" in input_data and not isinstance(input_data["wait_time"], int):
            raise ValueError("Wait time must be an integer")

        if "full_page" in input_data and not isinstance(input_data["full_page"], bool):
            raise ValueError("Full page must be a boolean")
