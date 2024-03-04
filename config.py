import json

from typing import TypedDict, TypeVar
from utils.logging import Color, log


class _HotkeyStyleConfig(TypedDict):
    is_horizontal: bool
    chin_color: str
    shadow_color: str
    text_color: str
    subtext_color: str
    border_color: str
    background_color: str
    animation_duration: str
    animation_delay: str
    font_size: str


class Config(TypedDict):
    port: int
    hotkey_style: _HotkeyStyleConfig
    hotkeys: list[str]


_DEFAULT_CONFIG: Config = Config(
    port=8000,
    hotkey_style=_HotkeyStyleConfig(
        is_horizontal=True,
        chin_color="#d9d9d9",
        shadow_color="#adb5bd",
        text_color="#343a40",
        subtext_color="#777",
        border_color="#e6e6e6",
        background_color="#fff",
        animation_duration="1s",
        animation_delay="5s",
        font_size="25px",
    ),
    hotkeys=[
        "ctrl+s",
        "ctrl+l",
        "ctrl+shift+a",
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
        "ctrl+shift+d",
        "ctrl+shift+f",
        "f6",
        "ctrl+p",
        "ctrl+shift+p",
    ],
)


def _load_config(filename: str) -> Config:
    # load the config from the specified file
    config = {}
    try:
        config = json.load(open(filename, "r"))
    except json.decoder.JSONDecodeError as e:
        log(f"Failed to parse the config file: {e}.", Color.RED)
        log(
            "Consider deleting the config.json file to create a new default config.",
            Color.YELLOW,
        )
        raise SystemExit
    except FileNotFoundError:
        log("No config.json found, creating a default config.", Color.YELLOW)

    # ensure default values for all unset properties recursively (sub-dicts)
    _set_defaults_recursive(config, _DEFAULT_CONFIG)

    # save the config in order to add properties missing in the file with their default values
    json.dump(config, open(filename, "w"), indent=4)

    return Config(Config(**config))


T = TypeVar("T", bound=dict)


def _set_defaults_recursive(dictionary: T, default: T) -> None:
    # set the default value for all items of the specified defaults
    for key, value in default.items():
        dictionary.setdefault(key, value)

        # if the value is a sub-dictionary, handle it recursively
        if isinstance(value, dict):
            dictionary.setdefault(key, {})
            _set_defaults_recursive(dictionary[key], value)


config: Config = _load_config("config.json")
