import asyncio
import keyboard
import config

from typing import TypedDict
from datetime import datetime
from quart import Quart, render_template, websocket


class HotkeyEvent(TypedDict):
    hotkey: str
    timestamp: datetime


app: Quart = Quart(__name__)
hotkey_events_ws_queues: set[asyncio.Queue[HotkeyEvent]] = set()


@app.get("/")
async def get():
    # serve the visualizer webpage
    return await render_template("visualizer.html", config=config.config)


@app.websocket("/")
async def ws():
    # accept the websocket connection and add a new event queue
    await websocket.accept()
    queue = asyncio.Queue()
    hotkey_events_ws_queues.add(queue)

    # handle the lifetime of the websocket connection
    try:
        while True:
           await websocket.send_json(await queue.get())
    finally:
        hotkey_events_ws_queues.remove(queue)


def register_keyboard_hooks() -> None:
    # register all shortcuts defined in the config
    for shortcut in config.config["shortcuts"]:
        keyboard.add_hotkey(shortcut, on_hotkey_callback, args=[HotkeyEvent(hotkey=shortcut, timestamp=datetime.utcnow())])  # type: ignore


def on_hotkey_callback(event: HotkeyEvent) -> None:
    # add the hotkey event to all queues
    for queue in hotkey_events_ws_queues:
        queue.put_nowait(event)


# start up
if __name__ == "__main__":
    config.load_config()
    register_keyboard_hooks()
    app.run()