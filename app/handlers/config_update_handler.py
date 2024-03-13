import time
import os
import sys
import watchdog.events
import watchdog.observers

from app.logging import Color, log


ignore_updates: bool = False
last_modified: float = 0


class _ConfigUpdateHandler(watchdog.events.FileSystemEventHandler):
    def on_modified(self, event: watchdog.events.FileSystemEvent) -> None:
        global last_modified
         
        # check whether the target file is our config file
        if not event.src_path.endswith("config.json"):
            return

        # ignore on_modified events fired <0.1s after the last one (bug in watchdog?)
        # or if we specifically told the update handler to ignore them
        if time.time() - last_modified < 0.1 or ignore_updates:
            return
        last_modified = time.time()

        log(f"{Color.LMAGENTA}config.json changed, reloading config...")
        os.execl(sys.executable, sys.executable, *sys.argv)


def run_update_listener():
    observer = watchdog.observers.Observer()
    observer.schedule(_ConfigUpdateHandler(), ".")
    observer.start()
