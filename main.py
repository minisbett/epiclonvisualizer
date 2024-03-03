import sys
import os.path
import json
import asyncio
import keyboard
import requests
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
        log(
            f"Serving app @ http://localhost:{config.config['server_configuration']['port']}/",
            Color.MAGENTA,
        )


async def main() -> None:
    # register all configured hotkey hooks
    register_hotkey_hooks(asyncio.get_running_loop())

    # setup hypercorn
    hconf = hypercorn.config.Config()
    hconf.bind = f"localhost:{config.config['server_configuration']['port']}"
    hconf.errorlog = None
    await hypercorn.asyncio.serve(app, hconf)


def update_check() -> None:
    # ignore update checks on local executions
    if not getattr(sys, "frozen", False):
        log("Running locally, skipping update checks.")
        return

    log("Checking for updates...")
    try:
        # get the latest release tag from the github api
        url = "https://api.github.com/repos/minisbett/epiclonvisualizer/releases/latest"
        newest_version = json.loads(requests.get(url).content)["tag_name"]
        log(f"Latest version: {newest_version}")
        
        # get the tag name this app version is from from the version.txt file bundled in the data-files (MEI folder)
        version = ""
        with open(os.path.join(sys._MEIPASS, "version.txt"), "r") as file: # type: ignore
            version = file.read()
            
        # notify the result
        if newest_version == version:
            log("You are using the latest version.")
        else:
            log(f"A newer version is available ({version} -> {newest_version})")
            log("You can download it here: https://github.com/minisbett/epiclonvisualizer")
            
    except Exception as e:
        log(f"Could not check for updates: {e}", Color.RED)
        pass


# start up
if __name__ == "__main__":
    update_check()

    # load the config and run the app
    config.load_config()
    asyncio.run(main())
