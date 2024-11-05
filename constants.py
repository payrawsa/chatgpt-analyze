# constants.py
import ctypes
from ctypes import wintypes
import pyautogui

# Load the user32 library
user32 = ctypes.windll.user32

# Define the function signature
SetWindowDisplayAffinity = user32.SetWindowDisplayAffinity
SetWindowDisplayAffinity.argtypes = [wintypes.HWND, wintypes.DWORD]
SetWindowDisplayAffinity.restype = wintypes.BOOL

# Define the display affinity constants
WDA_EXCLUDEFROMCAPTURE = 0x00000011
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x80000
WS_EX_TRANSPARENT = 0x20
WS_EX_NOACTIVATE = 0x8000000  # Allows the window to be click-through

code_question = lambda lang : f"Answer the coding question in {lang}. Using bullet points, shortly explain the intuition of the best solution and then show the code with a return value without comments."
SYSTEM_DESIGN = "Answer the system design question. Begin by defining if sql or nosql and define the schema if sql or document if nosql. Use existing technologies whenever possible instead of generalities. Try to explain why you use one technology over another. Make sure to follow the requirements, if any. Then draw a system design diagram."
SOLVE_AI = "Answer the problem. Begin by defining the problem in a short sentence. Then explain your approach in 1-4 bullet points. Then the solution. Add a diagram if useful. Then a small summary at the end. Avoid generalities and try to be specific with the solution."
HOTKEYS = """
Hide: alt+ctrl+h

Clickable: alt+ctrl+c

Solve: alt+ctrl+s

Move to Mouse: ctrl+shift
"""
# Static window dimensions
STATIC_HEIGHT = int(pyautogui.size().height*0.8)
STATIC_WIDTH = 1400