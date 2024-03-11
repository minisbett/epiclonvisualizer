import asyncio
import hypercorn.asyncio
import hypercorn.config
import app.utils
import app.config
import app.handlers.web_handler
import app.handlers.hotkey_handler
import app.logging

from quart import Quart
from app.logging import Color, log


quart: Quart = Quart(__name__)
quart.register_blueprint(app.handlers.web_handler.blueprint)


@quart.before_serving
async def before_serving():
    async with quart.test_request_context(""):
        log(
            f"{Color.MAGENTA}Serving app @ http://localhost:{app.config.config['port']}/"
        )


async def main() -> None:
    # setup logging
    app.logging.initialize()

    # run update checks
    await app.utils.run_update_check()
    
    # load the config and run the app
    app.config.load()

    # register all configured hotkey hooks
    app.handlers.hotkey_handler.register_hotkey_hooks(asyncio.get_running_loop())

    # setup hypercorn
    hconf = hypercorn.config.Config()
    hconf.bind = f"localhost:{app.config.config['port']}"
    hconf.errorlog = None
    await hypercorn.asyncio.serve(quart, hconf)


asyncio.run(main())
