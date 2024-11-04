from ai import capture_and_process_screenshot
from constants import CODE_QUESTION, SOLVE_AI, SYSTEM_DESIGN
from responsewindow import ResponseWindow
import keyboard

response_window = ResponseWindow()

def code():
    response = capture_and_process_screenshot(CODE_QUESTION)
    response_window.update_text(response)

def design():
    response = capture_and_process_screenshot(SYSTEM_DESIGN)
    response_window.update_text(response)

def solve():
    response = capture_and_process_screenshot(SOLVE_AI)
    response_window.update_text(response)
    
keyboard.add_hotkey("alt+ctrl+1", code)
keyboard.add_hotkey("alt+ctrl+3", design)
keyboard.add_hotkey("alt+ctrl+s", solve)
keyboard.add_hotkey("alt+ctrl+c", response_window.toggle_clickable)
keyboard.add_hotkey("alt+ctrl+h", response_window.toggle_visibility)
response_window.run()