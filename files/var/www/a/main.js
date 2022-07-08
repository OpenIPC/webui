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
        // serve auto value on range form fields
        function toggleAuto(el) {
            const id = el.dataset.for;
            const p = $('#' + id);
            const r = $('#' + id + '-range');
            const s = $('#' + id + '-show');
            if (el.checked) {
                el.dataset.value = r.value;
                p.value = 'auto';
                r.disabled = true;
                s.textContent = '--';
            } else {
                p.value = el.dataset.value;
                r.value = p.value;
                r.disabled = false;
                s.textContent = p.value;
            }
        }

        $$('form').forEach(el => el.autocomplete = 'off');

        // For .warning and .danger buttons, ask confirmation on action.
        $$('.btn-danger, .btn-warning, .confirm').forEach(el => {
            // for input, find its parent form and attach listener to it submit event
            if (el.nodeName === "INPUT") {
                while (el.nodeName !== "FORM") el = el.parentNode
                el.addEventListener('submit', ev => (!confirm("Are you sure?")) ? ev.preventDefault() : null)
            } else {
                el.addEventListener('click', ev => (!confirm("Are you sure?")) ? ev.preventDefault() : null)
            }
        });

        $$('.refresh').forEach(el => el.addEventListener('click', refresh));

        // open links to external resources in a new window.
        $$('a[href^=http]').forEach(el => el.target = '_blank');

        // add auto toggle button and value display for range elements.
        $$('input[type=range]').forEach(el => {
            el.addEventListener('input', ev => {
                const id = ev.target.id.replace(/-range/, '');`1`
                $('#' + id + '-show').textContent = ev.target.value;
                $('#' + id).value = ev.target.value;
            })
        });

        $$('input.auto-value').forEach(el => {
            el.addEventListener('click', ev => toggleAuto(ev.target));
            toggleAuto(el);
        });

        // const resizeObserver = new ResizeObserver(entries => {
        //     entries.forEach(entry => {
        //         if (entry.target.clientHeight > document.documentElement.clientHeight / 2) {
        //             entry.target.classList.add("log-scroll");
        //             entry.target.scrollTo(0, entry.target.scrollHeight);
        //         }
        //     });
        // });
        // $$('pre').forEach(el => resizeObserver.observe(el));

        // show password when "show" checkbox is checked
        $$(".password input[type=checkbox]").forEach(el => {
            el.addEventListener('change', ev => {
                const pw = $('#' + ev.target.dataset['for']);
                pw.type = (el.checked) ? 'text' : 'password';
                pw.focus();
            });
        });

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
                    if ("true" === el.dataset["reboot"]) {
                        window.location.href = '/cgi-bin/reboot.cgi'
                    } else {
                        el.innerHTML += '\n--- finished ---\n';
                    }
                }
            }
            async function run() {
                for await (let line of makeTextFileLineIterator('/cgi-bin/jrun.cgi?cmd=' + btoa(el.dataset["cmd"]))) {
                    const re1 = /\[1;(\d+)m/;
                    const re2 = /\[0m/;
                    line=line.replace(re1, '<span class="ansi-$1">').replace(re2, '</span>')
                    el.innerHTML += line + '\n';
                }
            }
            run()
        }
    }

    window.addEventListener('load', initAll);
})();
