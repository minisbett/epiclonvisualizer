import pystray
import threading
import ctypes
import app.config

from win32.lib.win32con import * # type: ignore
from PIL import Image
from app.logging import log


_WS_INVISIBLE = WS_OVERLAPPED | ~WS_THICKFRAME | ~WS_DLGFRAME | ~WS_VISIBLE


def _show_app():
    # show the app by setting the window styles back to default
    ctypes.windll.user32.SetWindowLongA(ctypes.windll.user32.GetForegroundWindow(), GWL_STYLE, WS_OVERLAPPED)
    ctypes.windll.user32.ShowWindow(ctypes.windll.user32.GetForegroundWindow(), SW_SHOW)


tray: pystray.Icon = pystray.Icon("Epic Lon Visualizer", Image.open("ext/icon.ico"), menu=pystray.Menu(
    pystray.MenuItem("Open...", action=_show_app, default=True)
))
tray_thread = threading.Thread(target=tray.run, daemon=True)


async def run() -> None:
    # run the system tray thread
    tray_thread.start()
    ctypes.windll.user32.SetWindowLongA(ctypes.windll.user32.GetForegroundWindow(), GWL_STYLE, _WS_INVISIBLE)
    ctypes.windll.user32.ShowWindow(ctypes.windll.user32.GetForegroundWindow(), SW_HIDE)