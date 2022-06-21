function reqListener() {
    console.log(this.responseText);
}

function sendToApi(endpoint) {
    const xhr = new XMLHttpRequest();
    xhr.addEventListener("load", reqListener);
    xhr.open("GET", "http://" + ipaddr + endpoint);
    xhr.setRequestHeader("Authorization", "Basic " + btoa("admin:"));
    xhr.send();
}

function initControls() {
    $$("a[id^=pan-],a[id^=zoom-]").forEach(el => {
        el.addEventListener("click", event => {
            event.preventDefault();
            alert("Sorry, this feature does not work, yet!");
        });
    });

    if ($("#night-mode")) $("#night-mode").addEventListener("click", event => {
        event.preventDefault();
        event.target.src = (event.target.src.split("/").pop() == "light-on.svg") ? "/a/light-off.svg" : "/a/light-on.svg";
        // sendToApi("/night/toggle");
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/cgi-bin/night.cgi");
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.send("mode=toggle");
    });

    if ($("#speed")) $("#speed").addEventListener("click", event => {
        event.preventDefault();
        event.target.src = (event.target.src.split("/").pop() == "speed-slow.svg") ? "/a/speed-fast.svg" : "/a/speed-slow.svg";
        // sendToApi("/speed/toggle");
    });
}

window.addEventListener("load", initControls);
