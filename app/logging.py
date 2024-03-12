import colorama

import threading
import tkinter as tk
from tkinter import scrolledtext

from enum import IntEnum
from datetime import datetime


# console color codes
class Color(IntEnum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37

    GRAY = 90
    LRED = 91
    LGREEN = 92
    LYELLOW = 93
    LBLUE = 94
    LMAGENTA = 95
    LCYAN = 96
    LWHITE = 97

    RESET = 0

    def __str__(self) -> str:
        return f"\x1b[{self.value}m"
    

def initialize() -> None:
    # Colorama provides ANSI support for coloring in the console
    colorama.init()
    # Just in case you're running on Windows
    colorama.just_fix_windows_console()

def log_to_tk(msg: str, text_widget: scrolledtext.ScrolledText) -> None:
    # Appends the specified message with a timestamp to the text widget
    colored_msg = f"{Color.GRAY}[{datetime.now().strftime('%H:%M:%S')}] {Color.RESET}{msg}{Color.RESET}"
    text_widget.insert('end', colored_msg + '\n')
    text_widget.see(tk.END)  # Scroll to the end to always show the latest message

def log(msg: str) -> None:
    global text_widget
    if 'text_widget' in globals():
        log_to_tk(msg, text_widget)
    else:
        print("Text widget not initialized yet. Skipping log message.")

# Tkinter GUI setup
def create_gui() -> None:
    global text_widget
    root = tk.Tk()
    root.title("Log Viewer")
    text_widget = scrolledtext.ScrolledText(root, wrap="word")
    text_widget.pack(expand=True, fill="both")
    initialize()
    root.mainloop()
    
def start_logger() -> None:
    gui_thread = threading.Thread(target=create_gui, daemon=True)
    gui_thread.start()