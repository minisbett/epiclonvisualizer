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
    "is_horizontal": True,
    "shortcuts": DEFAULT_SHORTCUTS
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