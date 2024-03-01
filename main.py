import keyboard
import config

from typing import TypedDict, Any
from datetime import datetime, timedelta
from quart import Quart, render_template


class HotkeyEvent(TypedDict):
    hotkey: str
    timestamp: datetime


app: Quart = Quart(__name__)
hotkey_events: list[HotkeyEvent] = []


@app.template_global("config")
def config_global() -> dict[str, Any]:
    return config.config


@app.get("/")
async def get():
    # serve the visualizer webpage
    return await render_template("visualizer.html")


@app.get("/events")
async def data():
    # get all events and clear them afterwards since they're "read"
    data = hotkey_events.copy()
    hotkey_events.clear()
    return data


def register_keyboard_hooks() -> None:
    # register all shortcuts defined in the config
    for shortcut in config.config["shortcuts"]:
        keyboard.add_hotkey(shortcut, on_hotkey_callback, args=[shortcut])  # type: ignore


def on_hotkey_callback(shortcut: str) -> None:
    # add the hotkey event
    print(shortcut)
    hotkey_events.append(HotkeyEvent(hotkey=shortcut, timestamp=datetime.utcnow()))

    # remove all hotkeys older than 30 seconds in case data isn't requested for a longer period
    for event in hotkey_events:
        if datetime.utcnow() - event["timestamp"] > timedelta(seconds=30):
            hotkey_events.remove(event)


# start up
if __name__ == "__main__":
    config.load_config()
    register_keyboard_hooks()
    app.run()