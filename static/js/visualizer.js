let hotkeys_container;
let lastHotkey;
let combo = 1;

window.addEventListener('load', async () => {
    hotkeys_container = document.getElementById("hotkeys-container");
    connect();
});

function connect() {
    console.log("Connecting");
    const ws = new WebSocket(`ws://localhost:${port || 8000}`);

    ws.onopen = () => console.log("Websocket connected.");

    ws.onerror = (error) => console.error("Websocket error: ", error);

    ws.onclose = () => {
        console.log("Websocket disconnected, reconnecting in 3 seconds...");
        setTimeout(connect, 3000);
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

        // delete all kbd elements with display: none, since they already disappeared
        for (let i = 0; i < hotkeys_container.children.length; i++)
            if (window.getComputedStyle(hotkeys_container.children[i]).display == "none")
                hotkeys_container.removeChild(hotkeys_container.children[i]);

        // check if the most recent hotkey is the same and the element for it still exists (so element count > 0)
        if (data.hotkey == lastHotkey && hotkeys_container.children.length > 0) {
            const last = hotkeys_container.lastChild;

            // increase the combo and modify the kbd::after content property through the combo attribute
            last.setAttribute("after-content", `${++combo}x`);

            // reset the fadeout animation on the kbd element
            last.style.animation = "none";
            void last.offsetWidth; // trigger reflow
            last.style.animation = "";
            return;
        }

        // if a maximum amount of simultaenous keys is set and we're at the maximum, delete the oldest one
        if ((max_keys || -1) > -1 && hotkeys_container.children.length == max_keys)
            hotkeys_container.removeChild(hotkeys_container.children[0])

        // otherwise, create a new kbd-element
        const elem = document.createElement("kbd");
        elem.innerHTML = lastHotkey = data.hotkey;
        hotkeys_container.appendChild(elem);
        combo = 1;
    };
}