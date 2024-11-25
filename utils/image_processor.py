import pyautogui
from PIL import Image
import pytesseract
from utils.api_client import APIClient

class ImageProcessor:
    def __init__(self, api_client: APIClient):
        self.is_running = False
        self.api_client = api_client

    def capture_and_process_screenshot(self, system: str):
        if self.is_running:
            return "Please wait for the previous request to finish."

        self.is_running = True
        try:
            # Capture screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save("output/screenshot.png")

            # Extract text from the screenshot using OCR
            img = Image.open("output/screenshot.png")
            user = pytesseract.image_to_string(img)

            # Get the response
            if user:  # Only proceed if there's text to analyze
                data = self.api_client.ask_chatgpt(system, user)
                return data.get("response")
            else:
                return "Nothing solvable was detected!"

        finally:
            self.is_running = False  # Reset the flag when done