import pyautogui
from PIL import Image
import pytesseract
from openai import OpenAI
from config import API_KEY  # Import API key from config.py

client = OpenAI(api_key=API_KEY)

class ScreenshotProcessor:
    def __init__(self):
        self.is_running = False

    def capture_and_process_screenshot(self, content: str):
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

            # Send the extracted text to the OpenAI API
            def ask_chatgpt(question, content):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": content},
                        {"role": "user", "content": question}
                    ]
                )
                return response.choices[0].message.content

            # Get the response
            if text:  # Only proceed if there's text to analyze
                return ask_chatgpt(text, content)
            else:
                return "Nothing solvable was detected!"

        finally:
            self.is_running = False  # Reset the flag when done
