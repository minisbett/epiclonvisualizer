import asyncio
import keyboard
import app.config
import app.handlers.web_handler

from typing import TypedDict
from datetime import datetime
from app.logging import Color, log


class HotkeyEvent(TypedDict):
    hotkey: str
    timestamp: datetime


def register_hotkey_hooks(loop: asyncio.AbstractEventLoop) -> None:
    # register all hotkeys defined in the config
    for hotkey in app.config.config["hotkeys"]:
        keyboard.add_hotkey(
            hotkey,
            lambda h=hotkey: asyncio.run_coroutine_threadsafe(
                _hotkey_callback(HotkeyEvent(hotkey=h, timestamp=datetime.utcnow())),
                loop,
            ),  # type: ignore
        )

    log(f"{Color.GREEN}Registered {len(app.config.config['hotkeys'])} hotkeys")


# the callback called via asyncio.run_coroutine_threadsafe, sending the event to connected websockets
async def _hotkey_callback(event: HotkeyEvent) -> None:
    log(f"{Color.LCYAN}Detected hotkey {Color.RESET}{event['hotkey']}")

    # add the hotkey event to all queues
    for queue in app.handlers.web_handler.ws_queues:
        queue.put_nowait(event)
