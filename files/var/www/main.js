let tock = 0;
let max = 0;

function $(n) {
    return document.querySelector(n);
}

function $$(n) {
    return document.querySelectorAll(n);
}

function tick() {
    tock += 1;
    $('#timer').value = tock;
    (tock === max) ? window.location.replace("/cgi-bin/status.cgi") : setTimeout(tick, 1000);
}

function engage() {
    max = $('#timer').max;
    setTimeout(tick, 1000);
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

        $$('input[data-for]').forEach(el => el.addEventListener('click', ev => toggleAuto(ev.target)));
        $$('select').forEach(el => el.autocomplete = 'off');
        $$('.btn-danger').forEach(el => el.addEventListener('click', ev => (!confirm("Are you sure?")) ? ev.preventDefault() : null));
        $$('a[href^=http]').forEach(el => el.target = '_blank');
    }

    window.onload = initAll;
})();
