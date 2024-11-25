import os
import keyboard
from dotenv import load_dotenv
from utils.image_processor import ImageProcessor
from utils.record import Recording
from utils.api_client import APIClient
from ui.responsewindow import ResponseWindow


def load_environment_variables():
    """Loads environment variables from the .env file."""
    load_dotenv()
    environment = os.getenv("ENVIRONMENT", "local")  # Default to "local" if not set
    base_url = os.getenv("BASE_URL", "http://localhost:8000")  # Default for local development
    print(f"Running in {environment} environment with base URL: {base_url}")
    return environment, base_url


def initialize_components(base_url):
    """Initializes application components."""
    api_client = APIClient(base_url)
    image_processor = ImageProcessor(api_client)
    response_window = ResponseWindow(image_processor)
    recorder = Recording(api_client)
    return image_processor, response_window, recorder


def setup_hotkeys(response_window, image_processor, recorder):
    """Sets up keyboard hotkeys for application functionalities."""
    keyboard.add_hotkey("ctrl+alt+s", lambda: solve(image_processor, response_window))
    keyboard.add_hotkey("ctrl+alt+c", response_window.toggle_clickable)
    keyboard.add_hotkey("ctrl+alt+h", response_window.toggle_visibility)
    keyboard.add_hotkey("ctrl+alt+r", lambda: toggle_recording(recorder, response_window))


def solve(image_processor, response_window):
    """Handles the screenshot capture and processing workflow."""
    if image_processor.is_running:
        response_window.update_text(
            "Please wait for your previous request to finish before making new ones!\n\nLOADING..."
        )
        return

    response_window.update_text(
        "Loading response. This will only take a moment!\n\nLOADING..."
    )
    response = image_processor.capture_and_process_screenshot(response_window.solution_mode)
    response_window.update_text(response)


def toggle_recording(recorder, response_window):
    """Toggles the recording state: starts if stopped, stops if recording."""
    if recorder.is_recording:
        response = recorder.stop_recording()
        response_window.update_text(response)
    else:
        recorder.start_recording()

def main():
    """Main entry point of the application."""
    # Load environment variables
    _, base_url = load_environment_variables()

    # Initialize components
    image_processor, response_window, recorder = initialize_components(base_url)

    # Setup keyboard hotkeys
    setup_hotkeys(response_window, image_processor, recorder)

    # Run the UI
    response_window.run()


if __name__ == "__main__":
    main()
