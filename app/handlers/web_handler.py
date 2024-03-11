import asyncio
import app.config

from quart import Blueprint, render_template, websocket
from app.logging import Color, log


blueprint: Blueprint = Blueprint("web_handler", __name__)
ws_queues: set[asyncio.Queue] = set()


@blueprint.get("/")
async def get():
    # serve the visualizer webpage
    return await render_template(
        "visualizer.html",
        style_config=app.config.config["hotkey_style"],
        port=app.config.config["port"],
    )


@blueprint.websocket("/")
async def ws():
    # accept the websocket connection and add a new payload queue
    await websocket.accept()
    queue = asyncio.Queue()
    ws_queues.add(queue)

    log(f"{Color.GREEN}Websocket connection established")

    # handle the lifetime of the websocket connection
    try:
        while True:
            await websocket.send_json(await queue.get())
    finally:
        ws_queues.remove(queue)
        log(f"{Color.RED}Websocket disconnected")
