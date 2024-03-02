import asyncio
import keyboard
import hypercorn.asyncio
import hypercorn.config
import config

from datetime import datetime
from quart import Quart, render_template, websocket, request
from objects.hotkey_event import HotkeyEvent
from utils.logging import Color, log, printc


app: Quart = Quart(__name__)
hotkey_events_ws_queues: set[asyncio.Queue[HotkeyEvent]] = set()


def register_hotkey_hooks(loop: asyncio.AbstractEventLoop) -> None:
    # the callback called via asyncio.run_coroutine_threadsafe, sending the event to connected websockets
    async def hotkey_callback(event: HotkeyEvent) -> None:
        log("Detected hotkey ", Color.LCYAN, nl=False)
        printc(event["hotkey"])

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
            ),  # type: ignore
        )

    log(f"Registered {len(config.config['hotkeys'])} hotkeys", Color.GREEN)


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

    log("Websocket connection established", Color.GREEN)

    # handle the lifetime of the websocket connection
    try:
        while True:
            event = await queue.get()
            await websocket.send_json(event)
    finally:
        hotkey_events_ws_queues.remove(queue)
        log("Websocket disconnected", Color.RED)
        
        
@app.before_serving
async def before_serving():
    async with app.test_request_context(""):
        log(f"Serving app @ http://localhost:{config.config['server_configuration']['port']}/", Color.MAGENTA)
    

async def main() -> None:
    # register all configured hotkey hooks
    register_hotkey_hooks(asyncio.get_running_loop())

    # setup hypercorn
    hconf = hypercorn.config.Config()
    hconf.bind = f"localhost:{config.config['server_configuration']['port']}"
    hconf.errorlog = None
    await hypercorn.asyncio.serve(app, hconf)


# start up
if __name__ == "__main__":
    config.load_config()
    asyncio.run(main())
