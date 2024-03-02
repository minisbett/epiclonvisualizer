import asyncio
import keyboard
import hypercorn.asyncio
import hypercorn.config
import config

from datetime import datetime
from quart import Quart, render_template, websocket
from objects.hotkey_event import HotkeyEvent


app: Quart = Quart(__name__)
hotkey_events_ws_queues: set[asyncio.Queue[HotkeyEvent]] = set()


@app.get("/")
async def get():
    # serve the visualizer webpage
    return await render_template(
        "visualizer.html",
        style_config=config.config["hotkey_style"],
        port=config.config["server_configuration"]["port"],
    )


@app.websocket("/")
async def ws():
    # accept the websocket connection and add a new event queue
    await websocket.accept()
    queue = asyncio.Queue()
    hotkey_events_ws_queues.add(queue)

    # handle the lifetime of the websocket connection
    try:
        while True:
            event = await queue.get()
            await websocket.send_json(event)
    finally:
        hotkey_events_ws_queues.remove(queue)


def register_hotkey_hooks(loop: asyncio.AbstractEventLoop) -> None:
    # the callback called via asyncio.run_coroutine_threadsafe, sending the event to connected websockets
    async def hotkey_callback(event: HotkeyEvent) -> None:
        # add the hotkey event to all queues
        for queue in hotkey_events_ws_queues:
            queue.put_nowait(event)

    # register all hotkeys defined in the config
    for hotkey in config.config["hotkeys"]:
        keyboard.add_hotkey(
            hotkey,
            lambda h=hotkey: asyncio.run_coroutine_threadsafe(
                hotkey_callback(HotkeyEvent(hotkey=h, timestamp=datetime.utcnow())),
                loop,
            ),
        )


async def main() -> None:
    # register all configured hotkey hooks
    register_hotkey_hooks(asyncio.get_running_loop())

    # setup hypercorn
    hconf = hypercorn.config.Config()
    hconf.bind = f"127.0.0.1:{config.config['server_configuration']['port']}"
    await hypercorn.asyncio.serve(app, hconf)


# start up
if __name__ == "__main__":
    config.load_config()
    asyncio.run(main())