import asyncio
import keyboard
import hypercorn.asyncio
import hypercorn.config
import config

from queue import Queue
from typing import TypedDict
from datetime import datetime
from quart import Quart, render_template, websocket


class HotkeyEvent(TypedDict):
    hotkey: str
    timestamp: datetime


app: Quart = Quart(__name__)
hotkey_events_ws_queues: set[Queue[HotkeyEvent]] = set()


@app.get("/")
async def get():
    # serve the visualizer webpage
    return await render_template("visualizer.html", style_config=config.config["hotkey_style"], port=config.config["server_configuration"]["port"])


@app.websocket("/")
async def ws():
    # accept the websocket connection and add a new event queue
    await websocket.accept()
    queue = Queue()
    hotkey_events_ws_queues.add(queue)

    # handle the lifetime of the websocket connection
    try:
        while True:
            event = await asyncio.to_thread(queue.get)
            await websocket.send_json(event)
    finally:
        hotkey_events_ws_queues.remove(queue)


def register_keyboard_hooks() -> None:
    # register all shortcuts defined in the config
    for shortcut in config.config["shortcuts"]:
        keyboard.add_hotkey(shortcut, on_hotkey_callback, args=[HotkeyEvent(hotkey=shortcut, timestamp=datetime.utcnow())])  # type: ignore


def on_hotkey_callback(event: HotkeyEvent) -> None:
    # add the hotkey event to all queues
    for queue in hotkey_events_ws_queues:
        queue.put(event)


# start up
if __name__ == "__main__":
    config.load_config()
    register_keyboard_hooks()
    
    # setup hypercorn
    hconf = hypercorn.config.Config()
    hconf.bind = f"127.0.0.1:{config.config['server_configuration']['port']}"
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(hypercorn.asyncio.serve(app, hconf))