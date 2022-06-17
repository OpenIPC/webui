let max = 0;

function $(n) {
    return document.querySelector(n);
}

function $$(n) {
    return document.querySelectorAll(n);
}

function refresh() {
    window.location.reload();
}

(function () {
    function initAll() {
        function toggleAuto(el) {
            const el2 = $('#' + el.dataset.for);
            if (el.checked) {
                el.dataset.value = el2.value;
                el2.value = 'auto';
                el2.readOnly = true;
            } else {
                el2.value = el.dataset.value;
                el2.readOnly = false;
            }
        }

        $$('form').forEach(el => el.autocomplete = 'off');
        $$('input[data-for]').forEach(el => el.addEventListener('click', ev => toggleAuto(ev.target)));
        $$('.btn-danger, .btn-warning, .confirm').forEach(el => {
            el.addEventListener('click', ev => (!confirm("Are you sure?")) ? ev.preventDefault() : null);
        });
        $$('.refresh').forEach(el => el.addEventListener('click', refresh));
        $$('a[href^=http]').forEach(el => el.target = '_blank');
        $$('input.pat-host').forEach(el => el.pattern='^[a-zA-Z0-9-_.]+$');
        $$('input.pat-host-ip').forEach(el => el.pattern='^[a-zA-Z0-9-_.]+$');

        const resizeObserver = new ResizeObserver(entries => {
            entries.forEach(entry => {
                if (entry.target.clientHeight > document.documentElement.clientHeight/2) {
                    entry.target.classList.add("log-scroll");
                    entry.target.scrollTo(0, entry.target.scrollHeight);
                }
            });
        });
        $$('pre').forEach(el => resizeObserver.observe(el));

        if ($("#send-to-telegram")) {
            $("#send-to-telegram").addEventListener("click", event => {
                event.preventDefault();
                if (!confirm("Are you sure?")) return false;
                const xhr = new XMLHttpRequest();
                xhr.open("GET", "/cgi-bin/telegram-bot-send.cgi");
                xhr.send();
            });
        }

        if ($("#send-to-yadisk")) {
            $("#send-to-yadisk").addEventListener("click", event => {
                event.preventDefault();
                if (!confirm("Are you sure?")) return false;
                const xhr = new XMLHttpRequest();
                xhr.open("GET", "/cgi-bin/yadisk-bot-send.cgi");
                xhr.send();
            });
        }
    }

    window.addEventListener('load', initAll);
})();
