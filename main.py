from ai import ScreenshotProcessor
from constants import CODE_QUESTION, SOLVE_AI, SYSTEM_DESIGN
from responsewindow import ResponseWindow
import keyboard

response_window = ResponseWindow()
gen_ai = ScreenshotProcessor()
response_window.gen_ai = gen_ai

def code():
    if gen_ai.is_running:
        response_window.update_text("Please wait for your previous request to finish before making new ones!")
        return
    response_window.update_text("Loading response. This will only take a moment!")
    response = gen_ai.capture_and_process_screenshot(CODE_QUESTION)
    response_window.update_text(response)

def design():
    if gen_ai.is_running:
        response_window.update_text("Please wait for your previous request to finish before making new ones!")
        return
    response_window.update_text("Loading response. This will only take a moment!")
    response = gen_ai.capture_and_process_screenshot(SYSTEM_DESIGN)
    response_window.update_text(response)

def solve():
    if gen_ai.is_running:
        response_window.update_text("Please wait for your previous request to finish before making new ones!")
        return
    response_window.update_text("Loading response. This will only take a moment!")
    response = gen_ai.capture_and_process_screenshot(SOLVE_AI)
    response_window.update_text(response)
    
keyboard.add_hotkey("alt+ctrl+1", code)
keyboard.add_hotkey("alt+ctrl+3", design)
keyboard.add_hotkey("alt+ctrl+s", solve)
keyboard.add_hotkey("alt+ctrl+c", response_window.toggle_clickable)
keyboard.add_hotkey("alt+ctrl+h", response_window.toggle_visibility)
response_window.run()