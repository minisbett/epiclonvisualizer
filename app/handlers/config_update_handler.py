import os
import sys
import watchdog.events
import watchdog.observers


class _ConfigUpdateHandler(watchdog.events.FileSystemEventHandler):
    def on_modified(self, event: watchdog.events.FileSystemEvent) -> None:
        print("detected config change")
        if event.src_path.endswith("config.json"):
            super().on_modified(event)
            os.execl(sys.executable, sys.executable, *sys.argv) 


def run_update_listener():
    observer = watchdog.observers.Observer()
    observer.schedule(_ConfigUpdateHandler(), ".")
    observer.start()
