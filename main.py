import asyncio
import json
import keyboard
import config

from queue import Queue
from typing import TypedDict, Any
from datetime import datetime, timedelta
from quart import Quart, Websocket, render_template, copy_current_websocket_context, websocket


class HotkeyEvent(TypedDict):
    hotkey: str
    timestamp: datetime


app: Quart = Quart(__name__)
hotkey_events_ws_queues: set[asyncio.Queue[HotkeyEvent]] = set()


@app.template_global("config")
def config_global() -> dict[str, Any]:
    return config.config


@app.get("/")
async def get():
    # serve the visualizer webpage
    return await render_template("visualizer.html")


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
    # add the hotkey event
    for queue in hotkey_events_ws_queues:
        asyncio.run(queue.put(event))


# start up
if __name__ == "__main__":
    config.load_config()
    register_keyboard_hooks()
    app.run()
