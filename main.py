import sys
import os.path
import json
import asyncio
import keyboard
import requests
import hypercorn.asyncio
import hypercorn.config

from datetime import datetime
from quart import Quart, render_template, websocket, request
from objects.hotkey_event import HotkeyEvent
from utils.logging import Color, log, printc
from config import config


GITHUB_REPOSITORY: str = "minisbett/epiclonvisualizer"

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
    for hotkey in config["hotkeys"]:
        keyboard.add_hotkey(
            hotkey,
            lambda h=hotkey: asyncio.run_coroutine_threadsafe(
                hotkey_callback(HotkeyEvent(hotkey=h, timestamp=datetime.utcnow())),
                loop,
            ),  # type: ignore
        )

    log(f"Registered {len(config['hotkeys'])} hotkeys", Color.GREEN)


@app.get("/")
async def get():
    # serve the visualizer webpage
    return await render_template(
        "visualizer.html",
        style_config=config["hotkey_style"],
        port=config["port"],
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
            f"Serving app @ http://localhost:{config['port']}/",
            Color.MAGENTA,
        )


async def main() -> None:
    # register all configured hotkey hooks
    register_hotkey_hooks(asyncio.get_running_loop())

    # setup hypercorn
    hconf = hypercorn.config.Config()
    hconf.bind = f"localhost:{config['port']}"
    hconf.errorlog = None
    await hypercorn.asyncio.serve(app, hconf)


def update_check() -> None:
    # get the latest release tag from the github api
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/releases/latest"
    newest_version = json.loads(requests.get(url).content)["tag_name"]
    log(f"Latest version: {newest_version}")
    
    # compare the fetched tag name with the version.txt file bundled in the data-files (MEI folder)
    with open(os.path.join(sys._MEIPASS, "version.txt"), "r") as file:  # type: ignore
        version = file.read()
        if newest_version == version:
            log("You are using the latest version.")
        else:
            log(f"A newer version is available ({version} -> {newest_version})")
            log(f"You can download it here: https://github.com/{GITHUB_REPOSITORY}")


# do an update check and run the app
if __name__ == "__main__":
    # ignore update checks on local executions (as opposed to PyInstaller executables)
    if not getattr(sys, "frozen", False):
        log("Running locally, skipping update checks.")
    else:
        try:
            log("Checking for updates...")
            update_check()
        except Exception as e:
            log(f"Could not check for updates: {e}", Color.RED)
            pass

    asyncio.run(main())
