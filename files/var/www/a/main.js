let max = 0;

function $(n) {
    return document.querySelector(n)
}

function $$(n) {
    return document.querySelectorAll(n)
}

function refresh() {
    window.location.reload()
}

(function () {
    function initAll() {
        function toggleAuto(el) {
            const el2 = $('#' + el.dataset.for);
            if (el.checked) {
                el.dataset.value = el2.value;
                el2.value = 'auto';
                el2.disabled = true
                $('#' + el2.id + '-value').textContent = 'auto';
            } else {
                el2.value = el.dataset.value;
                el2.disabled = false;
                $('#' + el2.id + '-value').textContent = el2.value;
            }
        }

        $$('form').forEach(el => el.autocomplete = 'off');

        $$('.btn-danger, .btn-warning, .confirm').forEach(el =>
            el.addEventListener('click', ev =>
                (!confirm("Are you sure?")) ? ev.preventDefault() : null));

        $$('.refresh').forEach(el => el.addEventListener('click', refresh));

        $$('a[href^=http]').forEach(el => el.target = '_blank');

        $$('input.auto-value').forEach(el => {
            el.addEventListener('click', ev => toggleAuto(ev.target));
            toggleAuto(el);
        });

        // add patterns
        $$('input.pat-host').forEach(el => el.pattern = '^[a-zA-Z0-9-_.]+$');

        $$('input.pat-host-ip').forEach(el => el.pattern = '^[a-zA-Z0-9-_.]+$');

        $$('input[type=range]').forEach(el =>
            el.addEventListener('input', ev =>
                $('#' + ev.target.id + '-value').textContent = ev.target.value));

        // const resizeObserver = new ResizeObserver(entries => {
        //     entries.forEach(entry => {
        //         if (entry.target.clientHeight > document.documentElement.clientHeight / 2) {
        //             entry.target.classList.add("log-scroll");
        //             entry.target.scrollTo(0, entry.target.scrollHeight);
        //         }
        //     });
        // });
        // $$('pre').forEach(el => resizeObserver.observe(el));

        $$(".password input[type=checkbox]").forEach(el =>
            el.addEventListener('change', ev =>
                $('#' + ev.target.dataset['for']).type = (el.checked) ? 'text' : 'password'));

        $("#send-to-telegram")?.addEventListener("click", event => {
            event.preventDefault();
            if (!confirm("Are you sure?")) return false;
            const xhr = new XMLHttpRequest();
            xhr.open("GET", "/cgi-bin/telegram-bot-send.cgi");
            xhr.send();
        });

        $("#send-to-yadisk")?.addEventListener("click", event => {
            event.preventDefault();
            if (!confirm("Are you sure?")) return false;
            const xhr = new XMLHttpRequest();
            xhr.open("GET", "/cgi-bin/yadisk-bot-send.cgi");
            xhr.send();
        });

        // async output of a command running on camera
        if ($('pre#output[data-cmd]')) {
            const el = $('pre#output[data-cmd]');
            async function* makeTextFileLineIterator(url) {
                const td = new TextDecoder('utf-8');
                const response = await fetch(url);
                const rd = response.body.getReader();
                let { value: chunk, done: readerDone } = await rd.read();
                chunk = chunk ? td.decode(chunk) : '';
                const re = /\n|\r|\r\n/gm;
                let startIndex = 0;
                let result;
                try {
                    for (;;) {
                        result = re.exec(chunk);
                        if (!result) {
                            if (readerDone) break;
                            let remainder = chunk.substr(startIndex);
                            ({value: chunk, done: readerDone} = await rd.read());
                            chunk = remainder + (chunk ? td.decode(chunk) : '');
                            startIndex = re.lastIndex = 0;
                            continue;
                        }
                        yield chunk.substring(startIndex, result.index);
                        startIndex = re.lastIndex;
                    }
                    if (startIndex < chunk.length) yield chunk.substr(startIndex);
                } finally {
                    if (el.dataset["reboot"] == "true") {
                        window.location.href = '/wait.html'
                    } else {
                        el.textContent += '\n--- finished ---\n';
                    }
                }
            }
            async function run() {
                for await (let line of makeTextFileLineIterator('/cgi-bin/jrun.sh?cmd=' + btoa(el.dataset["cmd"]))) {
                    el.textContent += line + '\n';
                }
            }
            run()
        }
    }

    window.addEventListener('load', initAll);
})();
