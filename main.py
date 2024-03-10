import asyncio
import hypercorn.asyncio
import hypercorn.config
import app.utils
import app.config
from app.handlers import web_handler, hotkey_handler, config_update_handler

from quart import Quart
from app.logging import Color, log


quart: Quart = Quart(__name__)
quart.register_blueprint(web_handler.blueprint)


@quart.before_serving
async def before_serving():
    async with quart.test_request_context(""):
        log(
            f"Serving app @ http://localhost:{app.config.config['port']}/",
            Color.MAGENTA,
        )


async def main() -> None:
    # load the config and run the config update listener
    app.config.load()
    config_update_handler.run_update_listener()

    # register all configured hotkey hooks
    hotkey_handler.register_hotkey_hooks(asyncio.get_running_loop())

    # setup hypercorn
    hconf = hypercorn.config.Config()
    hconf.bind = f"localhost:{app.config.config['port']}"
    hconf.errorlog = None
    await hypercorn.asyncio.serve(quart, hconf)


asyncio.run(main())
