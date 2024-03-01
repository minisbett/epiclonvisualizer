// fetches the hotkey events from the events endpoint
async function getHotkeyEvents() {
    const response = await fetch("http://localhost:5000/events").catch((e) => {
        console.error('error fetching data: ', e);
        return;
    })

    if (!response?.ok) {
        console.error(`error fetching data (${response?.status || "null"})`);
        return;
    }

    return await response.json().catch(() => { })
}

let hotkeys_container;
let lastHotkey;
let combo = 1;

async function loop() {
    // fetch the events and make sure to only proceed if successful
    hotkey_events = await getHotkeyEvents();
    if (hotkey_events)
        // go through all hotkey events and add a new kbd-element or increase the combo on the latest one
        hotkey_events.forEach(event => {
            // check if the most recent hotkey is the same and the element for it still exists (so element count > 0)
            if (event["hotkey"] == lastHotkey && hotkeys_container.children.length > 0) {
                const last = hotkeys_container.lastChild;

                // increase the combo and modify the kbd::after content property through the combo attribute
                last.setAttribute("combo", `x${++combo}`)
                
                // reset the fadeout animation on the kbd element and its ::after
                last.style.animation = "none";
                void last.offsetWidth; // trigger reflow
                last.style.animation = "";
                return;
            }

            // otherwise, create a new kbd-element
            const elem = document.createElement("kbd");
            elem.innerHTML = event["hotkey"];
            hotkeys_container.appendChild(elem);
            lastHotkey = event["hotkey"];
            combo = 1;
        });

    // delete all hotkey elements with display: none
    for (var i = 0; i < hotkeys_container.children.length; i++)
        if (window.getComputedStyle(hotkeys_container.children[i]).display == "none")
            hotkeys_container.removeChild(hotkeys_container.children[i]);
}

window.addEventListener('load', async () => {
    hotkeys_container = document.getElementById("hotkeys-container");

    // run the loop every 100ms
    setInterval(loop, 100);
});