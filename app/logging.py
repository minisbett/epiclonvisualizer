import colorama

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
    # colorama provides ANSI support for coloring in the console
    colorama.just_fix_windows_console()


def log(msg: str) -> None:
    # prints the specified message with a timestamp
    print(f"{Color.GRAY}[{datetime.now().strftime('%H:%M:%S')}] {Color.RESET}{msg}{Color.RESET}")
