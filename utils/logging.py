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

    def __repr__(self) -> str:
        return f"\x1b[{self.value}m"
    
def printc(msg: str, color: Color = Color.RESET, nl: bool = True) -> None:
    print(f"{color!r}{msg}{Color.RESET!r}", end="\n" if nl else "")

def log(msg: str, color: Color = Color.RESET, nl: bool = True) -> None:
    printc(f"[{datetime.now().strftime('%H:%M:%S')}] ", Color.GRAY, nl=False)
    printc(msg, color, nl)