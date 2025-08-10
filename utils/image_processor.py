import pyautogui
from PIL import Image
import pytesseract
from utils.api_client import APIClient

class ImageProcessor:
    def __init__(self, api_client: APIClient):
        self.is_running = False
        self.api_client = api_client

    def capture_and_process_screenshot(self, prompt: str, text: str, screenshot_mode: bool = False):
        if self.is_running:
            return "Please wait for the previous request to finish."

        self.is_running = True
        try:
            if screenshot_mode:
                # Capture screenshot
                screenshot = pyautogui.screenshot()
                screenshot.save("output/screenshot.png")
                # Capture screenshot
                screenshot = pyautogui.screenshot()
                screenshot.save("output/screenshot.png")

                # Extract text from the screenshot using OCR
                img = Image.open("output/screenshot.png")
                screenshot_text = pytesseract.image_to_string(img)

                # Get the response
                if screenshot_text:  # Only proceed if there's text to analyze
                    data = self.api_client.ask_chatgpt(prompt, screenshot_text)
                    return data.get("response")
                return "Nothing solvable was detected!"
            data = self.api_client.ask_chatgpt(prompt, text)
            return data.get("response")
        

        finally:
            self.is_running = False  # Reset the flag when done