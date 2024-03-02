<div align="center">

<img src=".github/assets/icon.png" />

# Log Off Now Hotkey Visualizer

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Downloads](https://img.shields.io/github/downloads/minisbett/epiclonvisualizer/total?style=flat&color=40b86b
)](https://github.com/minisbett/epiclonvisualizer/releases/latest)
[![Latest Release](https://img.shields.io/github/v/release/minisbett/epiclonvisualizer?color=ff5867
)](https://github.com/minisbett/epiclonvisualizer/releases/latest)

A lightweight and customizable websocket/browser-based hotkey visualizer,<br/>made specifically for [Log Off Now](https://twitch.tv/log_off_now)'s Twitch stream overlay.

[Demo](#demo) • [Usage](#usage) • [Configuration](#configuration) • [Development](#development)<br/>

<i>Made with ❤️ by @minisbett and @Omekyu</i>
</div>

## Usage
### Downloading and running the app

To get started, head over to the [latest release page](https://github.com/minisbett/epiclonvisualizer/releases/latest) on GitHub. From there, locate and download the executable file (<u>ending with `.exe`</u>).

Once the download is complete, simply double-click the downloaded executable file to launch the application. No installation is required, and the application will start automatically upon execution.

### Embedding in OBS

The application provides an out-of-the-box visualization webpage, running on `http://localhost:8000` by default.

If you're using OBS Studio to stream on the streaming platform of your choice, you can easily integrate the hotkey visualizer into your overlay. Here's how:

1. Open OBS Studio and navigate to the scene where you want to add the visualizer.
2. Click the "+" icon under the "Sources" section to add a new source.
3. Choose "Browser" as the source type and give it an appropriate name (e.g., "Hotkey Visualizer").
4. In the URL field, enter `http://localhost:8000` *(default, unless configured otherwise)*
5. For the width and height, choose suitable values to ensure the displayed hotkeys are fully visible and not cut off. *(e.g. 1000x100)*

### Using the websocket directly

All pressed hotkeys are being sent to a local websocket, which can be accessed via `ws://localhost:8000` by default. The payloads sent look as follows:
```json
{
     // as configured in the config, e.g. "ctrl+shift+p"
    "hotkey": "<hotkey>",
     // YYYY-MM-DD HH:MM:SS.microseconds
    "timestamp": "<timestamp>"
}
```

## Configuration

In the `config.json` file, you can customize the hotkeys to capture, the style of the visualizer and the port on which the application is running. 

On first startup, the application creates a `config.json` file in the same directory, containing the default configuration. After that, you are free to adjust all the values to your liking.

### Configuration options

#### Server Configuration

- **Port**: Specifies the port number on which the server runs. Default is 8000.

#### Hotkey Style

- **is_horizontal**: Determines the orientation of the hotkey display. When `true`, hotkeys are displayed horizontally, with the most recently pressed hotkey on the right. When `false`, hotkeys are displayed vertically, with the most recently pressed hotkey on the bottom.

- **chin-color**: Color of the chin (bottom border) of the hotkey.

- **shadow-color**: Color of the shadow around the hotkey.

- **text-color**: Color of the hotkey text displayed.

- **subtext-color**: Color of the "combo" text displayed.

- **border-color**: Color of the border around the hotkey.

- **background-color**: Background color of the hotkey.

- **animation-duration**: Duration of the fade-out animation.

- **animation-delay**: Delay before a hotkey fades out.

- **font-size**: Size of the font used for displaying hotkeys.

### Hotkeys

A list of the hotkeys that are being captured by the application. The key combination is written by the human-readable names of the keys, combined with a plus-sign. *(Examples: `ctrl+shift+p`, `shift+del`)*

The syntax for the hotkey-literals goes as follows: 
```
          alt+shift+a     alt+b, c
 Keys:    ^~^ ^~~~^ ^     ^~^ ^  ^
Steps:    ^~~~~~~~~~^     ^~~~^  ^
```
The first hotkey triggers when alt, shift and A are pressed at the same time. The second hotkey triggers when alt and B are pressed, followed by the key c as the second step afterwards.