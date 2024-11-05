from ai import ScreenshotProcessor
from responsewindow import ResponseWindow
import keyboard

response_window = ResponseWindow()
gen_ai = ScreenshotProcessor()
response_window.gen_ai = gen_ai

def solve():
    if gen_ai.is_running:
        response_window.update_text("Please wait for your previous request to finish before making new ones!\n\nLOADING... \n\nLOADING... \n\nLOADING...")
        return
    response_window.update_text("Loading response. This will only take a moment!\n\nLOADING... \n\nLOADING... \n\nLOADING...\n\nLOADING... \n\nLOADING... \n\nLOADING...")
    response = gen_ai.capture_and_process_screenshot(response_window.solution_mode)
    response_window.update_text(response)
    
keyboard.add_hotkey("alt+ctrl+s", solve)
keyboard.add_hotkey("alt+ctrl+c", response_window.toggle_clickable)
keyboard.add_hotkey("alt+ctrl+h", response_window.toggle_visibility)
response_window.run()