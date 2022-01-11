function reqListener() {
    console.log(this.responseText);
}

function sendToApi(endpoint) {
    const xhr = new XMLHttpRequest();
    xhr.addEventListener("load", reqListener);
    xhr.open("GET", "http://<%= $ipaddr %>" + endpoint);
    xhr.send();
}

function initControls() {
    $$('a[id^=pan-],a[id^=zoom-]').forEach(el => {
        el.addEventListener('click', event => {
            event.preventDefault();
            alert('Sorry, this feature does not work, yet!');
        });
    });

    if ($('#night-mode')) $('#night-mode').addEventListener('click', event => {
        event.preventDefault();
        event.target.src = (event.target.src.split('/').pop() == 'light-on.svg') ? '/img/light-off.svg' : '/img/light-on.svg';
        sendToApi('/night/toggle');
    });

    if ($('#send-to-telegram')) {
        $('#send-to-telegram').addEventListener('click', event => {
            event.preventDefault();
            if (!confirm('Are you sure?')) return false;
            const xhr = new XMLHttpRequest();
            xhr.open("GET", "/cgi-bin/telegram-bot-send.cgi");
            xhr.send();
        });
    }

    if ($('#speed')) $('#speed').addEventListener('click', event => {
        event.preventDefault();
        event.target.src = (event.target.src.split('/').pop() == 'speed-slow.svg') ? '/img/speed-fast.svg' : '/img/speed-slow.svg';
        // sendToApi('/speed/toggle');
    });
}

window.addEventListener('load', initControls);
