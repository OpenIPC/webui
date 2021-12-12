let tock = 0;
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
        $$('.btn-danger, .btn-warning, .confirm').forEach(el => el.addEventListener('click', ev => (!confirm("Are you sure?")) ? ev.preventDefault() : null));
        $$('.refresh').forEach(el => el.addEventListener('click', refresh));
        $$('a[href^=http]').forEach(el => el.target = '_blank');
        $$('input.pat-host').forEach(el => el.pattern='^[a-zA-Z0-9-_.]+$');
        $$('input.pat-host-ip').forEach(el => el.pattern='^[a-zA-Z0-9-_.]+$');
    }

    window.addEventListener('load', initAll);
})();
