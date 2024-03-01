import os.path
import json

from typing import Any


DEFAULT_SHORTCUTS: list[str] = [
    # file
    "ctrl+s",
    "ctrl+l",
    "ctrl+shift+a",
    
    # edit
    "ctrl+z",
    "ctrl+y",
    "ctrl+x",
    "ctrl+c",
    "ctrl+v",
    "del",
    "ctrl+a",
    "ctrl+d",
    "ctrl+g",
    "ctrl+h",
    "ctrl+j",
    "ctrl+>",
    "ctrl+<",
    "ctrl+shift+r",
    "ctrl+shift+s",

    #compose
    "ctrl+shift+d",
    "ctrl+shift+f",
    
    # timing
    "f6",
    "ctrl+p",
    "ctrl+shift+p"
]

default_config: dict[str, Any] = {
    "shortcuts": DEFAULT_SHORTCUTS,

    # direction
    "is_horizontal": True,

    # colors
    "chin-color": "#d9d9d9",
    "shadow-color": "#adb5bd",
    "text-color": "#343a40",
    "subtext-color": "#777",
    "border-color": "#e6e6e6",

    # animation settings
    "animation-duration": "1s",
    "animation-delay": "5s",

    # font size
    "font-size": "25px"
}

config: dict[str, Any] = {}

def load_config() -> None:
    global config
    if not os.path.isfile("config.json"):
        with open("config.json", "w") as file:
            json.dump(default_config, file, indent=2)
            config = default_config
    else:
        with open("config.json", "r") as file:
            config = json.load(file)