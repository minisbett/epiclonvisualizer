import pystray
import threading
import ctypes
import app.config
import win32gui
import time

from win32.lib.win32con import * # type: ignore
from PIL import Image
from app.logging import log


_WS_INVISIBLE = WS_OVERLAPPED | ~WS_THICKFRAME | ~WS_DLGFRAME | ~WS_VISIBLE
console_window = ctypes.windll.kernel32.GetConsoleWindow()

def _show_app():
    # show the app by setting the window styles back to default
    # ctypes.windll.user32.SetWindowLongA(ctypes.windll.user32.GetConsoleWindow(), GWL_STYLE, WS_OVERLAPPED)
    ctypes.windll.user32.ShowWindow(console_window, SW_SHOW)
    win32gui.ShowWindow(console_window, SW_NORMAL)
    
    # stopping the system tray
    tray.stop()
    

def _minimize():
    while True:
        if console_window:
            tup = win32gui.GetWindowPlacement(console_window)
            if tup[1] == SW_SHOWMINIMIZED:
                # run as soon as the window was minimized
                # ctypes.windll.user32.SetWindowLongA(ctypes.windll.kernel32.GetConsoleWindow(), GWL_STYLE, _WS_INVISIBLE)
                ctypes.windll.user32.ShowWindow(console_window, SW_HIDE)
                tray_thread.start()
                break
        time.sleep(1)


tray: pystray.Icon = pystray.Icon("Epic Lon Visualizer", Image.open("ext/icon.ico"), menu=pystray.Menu(
    pystray.MenuItem("Open...", action=_show_app, default=True)
))
tray_thread = threading.Thread(target=tray.run, daemon=True)
minimize_thread = threading.Thread(target=_minimize, daemon=True)

async def run() -> None:
    # run the minimize thread
    minimize_thread.start()