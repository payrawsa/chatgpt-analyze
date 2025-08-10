import os
import keyboard
from dotenv import load_dotenv
from utils.image_processor import ImageProcessor
from utils.record import Recording
from utils.api_client import APIClient
from ui.responsewindow import ResponseWindow
from utils.pdf_text_extract import PDFTextExtractor


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
    response_window = ResponseWindow(image_processor, api_client)
    recorder = Recording(api_client)
    pdf_extractor = PDFTextExtractor()
    return image_processor, response_window, recorder, pdf_extractor


def process_pdf_study_guide(api_client: APIClient, response_window: ResponseWindow):
    """Process PDF file to create study guide."""
    pdf_path = response_window.entry.get()
    print(pdf_path)
    if not pdf_path:
        response_window.update_text("Please enter a PDF file path in the entry field!")
        return
    
    response_window.update_text("Creating study guide from PDF... Please wait...")
    try:
        study_guide = create_study_guide(pdf_path, api_client, 215)
        # Create output filename based on input PDF name
        output_filename = os.path.splitext(os.path.basename(pdf_path))[0] + "_study_guide.txt"
        output_path = os.path.join("output", output_filename)
        
        # Save study guide to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(study_guide)
        
        response_window.update_text(f"Study guide created successfully! Saved to: {output_path}")
    except Exception as e:
        response_window.update_text(f"Error processing PDF: {str(e)}")

def setup_hotkeys(response_window, image_processor, recorder, api_client):
    """Sets up keyboard hotkeys for application functionalities."""
    keyboard.add_hotkey("ctrl+alt+s", lambda: solve(image_processor, response_window))
    keyboard.add_hotkey("ctrl+alt+c", response_window.toggle_clickable)
    keyboard.add_hotkey("ctrl+alt+h", response_window.toggle_visibility)
    keyboard.add_hotkey("ctrl+alt+r", lambda: toggle_recording(recorder, response_window))
    keyboard.add_hotkey("ctrl+alt+p", lambda: process_pdf_study_guide(api_client, response_window))


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

def create_study_guide(pdf_path: str, api_client: APIClient, max_pages: int = None) -> str:
    """
    Creates a study guide from a PDF file using OCR and AI analysis.
    Processes text in chunks of 10 pages to manage API requests better.
    
    Args:
        pdf_path (str): Path to the PDF file
        api_client (APIClient): Instance of APIClient for API calls
        max_pages (int, optional): Maximum number of pages to process
        
    Returns:
        str: Generated study guide
    """
    CHUNK_SIZE = 10  # Process 10 pages at a time
    pdf_extractor = PDFTextExtractor()
    all_study_guides = []
    chunk_number = 1
    
    # Create base prompt for the study guide
    base_prompt = """
    In ARABIC, Create a study guide for this section. The guide should be organized by
    topics and subtopics. Each topic and/or subtopic should be clearly defined.
    Include key concepts, definitions, and important quotes under each topic and subtopic.
    Minimum text should be about 25%\ of the input text.
    Response should be detailed and thorough.
    Use the text provided. DO NOT GIVE A SHORT RESPONSE!"""
    
    # Process PDF in chunks
    for start_page in range(1, max_pages + 1, CHUNK_SIZE):
        end_page = min(start_page + CHUNK_SIZE - 1, max_pages)
        print(f"\nProcessing pages {start_page} to {end_page}")
        
        # Extract text for this chunk
        chunk_text = pdf_extractor.get_text_from_pdf(pdf_path, max_pages=CHUNK_SIZE, start_page=start_page)
        
        # Save chunk text to file
        chunk_filename = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_text_chunk_{chunk_number}.txt"
        chunk_path = os.path.join("output", chunk_filename)
        with open(chunk_path, "w", encoding="utf-8") as f:
            f.write(chunk_text)
        print(f"Saved chunk {chunk_number} text to: {chunk_path}")
        
        # Create prompt for this chunk
        chunk_prompt = base_prompt.format(chunk=chunk_number)
        
        # Get AI-generated study guide for this chunk
        response = api_client.ask_chatgpt(chunk_prompt, chunk_text)
        if response.get("response"):
            all_study_guides.append(response["response"])
        else:
            print(f"Warning: Failed to generate study guide for pages {start_page}-{end_page}")
        
        chunk_number += 1
    
    # Combine all chunks into final study guide
    if not all_study_guides:
        return "Failed to generate study guide."
    
    final_guide = "\n\n" + "="*50 + "\n\n".join(all_study_guides)
    
    # Save complete study guide
    output_filename = os.path.splitext(os.path.basename(pdf_path))[0] + "_complete_study_guide.txt"
    output_path = os.path.join("output", output_filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_guide)
    
    return final_guide

def main():
    """Main entry point of the application."""
    # Load environment variables
    _, base_url = load_environment_variables()

    # Initialize components
    image_processor, response_window, recorder, pdf_extractor = initialize_components(base_url)

    # Setup keyboard hotkeys
    setup_hotkeys(response_window, image_processor, recorder, image_processor.api_client)

    # Run the UI
    response_window.run()


if __name__ == "__main__":
    main()
