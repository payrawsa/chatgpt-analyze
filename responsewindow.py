import pyautogui
import keyboard
import customtkinter
from constants import (  # Import constants
    SetWindowDisplayAffinity,
    user32,
    WDA_EXCLUDEFROMCAPTURE,
    GWL_EXSTYLE,
    WS_EX_LAYERED,
    WS_EX_TRANSPARENT,
    WS_EX_NOACTIVATE,
    STATIC_WIDTH,
    STATIC_HEIGHT,
    HOTKEYS,
    code_question,
    SYSTEM_DESIGN,
    SOLVE_AI
)

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ResponseWindow(customtkinter.CTk):
    def __init__(self, gen_ai):
        super().__init__()
        self.gen_ai = gen_ai

        # configure window
        self.title("ChatGPT Response") 
        self.attributes('-topmost', True)  # Keep the window always on top        
        screen_width, screen_height = pyautogui.size()
        x_position = (screen_width - STATIC_WIDTH) // 2  # Center horizontally
        y_position = (screen_height - STATIC_HEIGHT) // 2  # Center vertically
        self.wm_geometry(f"{STATIC_WIDTH}x{STATIC_HEIGHT}+{x_position}+{y_position}")
        self.clickable = False
        self.transparent = False
        self.language_mode = "Python"
        self.solution_mode =  code_question(self.language_mode)

        # configure grid layout (3x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)
        
        
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.toggle_transparent, text="Toggle Transparent")
        self.sidebar_button_1.grid(row=0, column=0, padx=20, pady=20)
        
        
        self.solution_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Solution Mode:", anchor="w")
        self.solution_mode_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.solution_mode_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Code", "Design", "General Solve"], command=self.change_solution_mode_event)
        self.solution_mode_optionmenu.grid(row=2, column=0, padx=20, pady=(10, 10))
        
        
        self.language_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Coding Language:", anchor="w")
        self.language_mode_label.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.language_mode_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Python", "Javascript", "Java"], command=self.change_language_mode_event)
        self.language_mode_optionmenu.grid(row=4, column=0, padx=20, pady=(10, 10))

        
        self.key_1 = customtkinter.CTkLabel(self.sidebar_frame, text=HOTKEYS, justify="left", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.key_1.grid(row=6, column=0, padx=(20,20))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=10, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=11, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Custom Prompt")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Send", command=self.customEntry)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=STATIC_WIDTH, height=STATIC_HEIGHT)
        self.textbox.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), columnspan=3, sticky="nsew")

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.textbox.insert("0.0", "Your answer will show here!")

        # Set up a timer to update the window position constantly
        self.update_position()

        # Attempt to get the window handle with retries
        self.max_retries = 20  # Number of attempts to find the window handle
        self.current_retry = 0
        self.after(100, self.get_window_handle)  # Start checking after 100 milliseconds
        

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_solution_mode_event(self, solution_mode: str):
        if solution_mode == "Code":
            self.solution_mode = code_question(self.language_mode)
        elif solution_mode == "Design":
            self.solution_mode = SYSTEM_DESIGN
        else:
            self.solution_mode = SOLVE_AI

    def change_language_mode_event(self, language_mode: str):
        self.language_mode = language_mode
        if self.solution_mode_optionmenu.get() == "Code":
            self.solution_mode = code_question(self.language_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def toggle_transparent(self):
        if self.transparent:
            self.transparent = False
            self.attributes('-alpha', 1.0)  # Set transparency (1.0 is fully opaque, 0.0 is fully transparent)
        else:
            self.transparent = True
            self.attributes('-alpha', 0.6)  # Set transparency (1.0 is fully opaque, 0.0 is fully transparent)
            

    def toggle_clickable(self):
        if not self.clickable:
            self.clickable = True
            self.make_clickable()
        else:
            self.clickable = False
            self.make_click_through()

    def get_window_handle(self):
        hwnd = user32.FindWindowW(None, "ChatGPT Response")
        if hwnd:
            # Set the display affinity
            SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
            self.make_click_through()
        else:
            self.current_retry += 1
            if self.current_retry < self.max_retries:
                # Try again after 100 milliseconds
                self.after(100, self.get_window_handle)
            else:
                self.update_text("Something happened. Please restart the application!")

    def make_click_through(self):
        hwnd = user32.FindWindowW(None, "ChatGPT Response")
        if hwnd:
            # Set layered and transparent styles along with no activate
            self.transparent = True
            self.attributes('-alpha', 0.6)  # Set transparency (1.0 is fully opaque, 0.0 is fully transparent)            
            styles = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            new_styles = styles | WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_NOACTIVATE
            user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_styles)

    def make_clickable(self):
        hwnd = user32.FindWindowW(None, "ChatGPT Response")
        if hwnd:
            # Remove the WS_EX_LAYERED, WS_EX_TRANSPARENT, and WS_EX_NOACTIVATE styles
            self.transparent = False
            self.attributes('-alpha', 1.0)  # Set transparency (1.0 is fully opaque, 0.0 is fully transparent)
            styles = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            new_styles = styles & ~WS_EX_TRANSPARENT
            user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_styles)

    def update_position(self):
        # Get the current mouse position
        mouse_x, _ = pyautogui.position()  # Only need the x position
        pos_y = self.winfo_y()
        # Move the window horizontally with the cursor while keeping the vertical position fixed
        new_x = mouse_x - STATIC_WIDTH // 2  # Center the window under the cursor

        if keyboard.is_pressed('ctrl+shift'):  # Check if the Shift key is pressed
            self.wm_geometry(f"{self.winfo_width()}x{self.winfo_height()}+{new_x}+{pos_y}")

        # Schedule the next position update
        self.after(10, self.update_position)  # Update position every 10 milliseconds

    def update_text(self, new_text):
        # Split the GPT response into individual lines
        self.textbox.delete("1.0", "end")  # Clear existing text
        self.textbox.insert("1.0", new_text)  # Insert the new text

    def toggle_visibility(self):
        if self.winfo_viewable():
            self.withdraw()  # Hide the window
        else:
            self.deiconify()  # Show the window

    def run(self):
        self.mainloop()

    def customEntry(self):
        if self.gen_ai.is_running:
            self.update_text("Please wait for your previous request to finish before making new ones!")
            return
        self.update_text("Loading response. This will only take a moment!")
        entry = self.entry.get()
        response = self.gen_ai.capture_and_process_screenshot(entry)
        self.update_text(response)
