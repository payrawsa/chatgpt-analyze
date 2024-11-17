import pyautogui
from PIL import Image
import pytesseract
from openai import OpenAI
from config import OPENAI_API_KEY  # Import API key from config.py



class ScreenshotProcessor:
    def __init__(self):
        self.is_running = False
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def capture_and_process_screenshot(self, question: str):
        if self.is_running:
            return "Please wait for the previous request to finish."

        self.is_running = True
        try:
            # Capture screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save("screenshot.png")

            # Extract text from the screenshot using OCR
            img = Image.open("screenshot.png")
            text = pytesseract.image_to_string(img)

            # Get the response
            if text:  # Only proceed if there's text to analyze
                return self.ask_chatgpt(text, question)
            else:
                return "Nothing solvable was detected!"

        finally:
            self.is_running = False  # Reset the flag when done

    def ask_chatgpt(self, content, question):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": question},
                {"role": "user", "content": content}
            ]
        )
        return response.choices[0].message.content
