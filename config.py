import os.path
import json

from typing import Any
from utils.logging import Color, log

DEFAULT_HOTKEYS: list[str] = [
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
    # compose
    "ctrl+shift+d",
    "ctrl+shift+f",
    # timing
    "f6",
    "ctrl+p",
    "ctrl+shift+p",
]

DEFAULT_STYLE = {
    # direction
    "is_horizontal": True,
    # colors
    "chin-color": "#d9d9d9",
    "shadow-color": "#adb5bd",
    "text-color": "#343a40",
    "subtext-color": "#777",
    "border-color": "#e6e6e6",
    "background-color": "#fff",
    # animation settings
    "animation-duration": "1s",
    "animation-delay": "5s",
    # font size
    "font-size": "25px"
}

default_config: dict[str, Any] = {
    "server_configuration": {
        "port": 8000
    },
    "hotkey_style": DEFAULT_STYLE,
    "hotkeys": DEFAULT_HOTKEYS
}

config: dict[str, Any] = {}


def load_config() -> None:
    global config
    if not os.path.isfile("config.json"):
        with open("config.json", "w") as file:
            json.dump(default_config, file, indent=2)
            config = default_config
            
        log("No config.json found, created default config", Color.YELLOW)
    else:
        try:
            with open("config.json", "r") as file:
                config = json.load(file)
        except json.decoder.JSONDecodeError as e:
            log(f"Failed to parse the config file: {e}.", Color.RED)
            log("Consider deleting it to create a default config.", Color.YELLOW)
            raise SystemExit
