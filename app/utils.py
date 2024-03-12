import sys
import json
import os.path
import requests
import pyautogui

from app.logging import Color, log


VERSION_TXT: str = os.path.join(getattr(sys, "_MEIPASS", ""), "version.txt")  # type: ignore
GH_LATEST: str = "minisbett/epiclonvisualizer/releases/latest"


async def run_update_check() -> None:
    # run an update check, but ignore them on local environments (not a PyInstaller executable)
    if not _is_pyinstaller_executable():
        log("Running locally, skipping update checks.")
        return

    log("Checking for updates...")

    # get the latest release
    if not (latest := await _get_latest_release()):
        return

    log(f"Latest version: {latest}")

    # compare the fetched tag name with the version.txt file bundled in the data-files (MEI folder)
    with open(VERSION_TXT, "r") as file:  # type: ignore
        if (version := file.read()) != latest:
            log(f"A newer version is available ({version} -> {latest})")
            log(f"You can download it here: https://github.com/{GH_LATEST}")
        else:
            log("You are using the latest version.")


async def _get_latest_release() -> str | None:
    try:
        # get the latest release tag from the github api
        response = requests.get(f"https://api.github.com/repos/{GH_LATEST}")
        return json.loads(response.content)["tag_name"]
    except Exception as e:
        log(f"{Color.RED}Update check failed: {e}")


def is_active_window_osu_editor() -> bool:
    title: str = pyautogui.getActiveWindowTitle()  # type: ignore
    return title.startswith("osu!  -") and title.endswith(".osu")


def _is_pyinstaller_executable() -> bool:
    return getattr(sys, "frozen", False)
