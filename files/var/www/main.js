function $(n) {
    return document.querySelector(n);
}

function $$(n) {
    return document.querySelectorAll(n);
}

let tock = 0;
let max = 0;

function tick() {
    tock += 1;
    $('#timer').value = tock;
    (tock === max) ? window.location.replace("/") : setTimeout(tick, 1000);
}

function engage() {
    max = $('#timer').max;
    setTimeout(tick, 1000);
}

(function () {
    // const patterns = {
    //     a: {
    //         rx: '^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
    //         msg: 'IPv4 address consists of four decimal numbers, each ranging from 0 to 255, separated by dots'
    //     },
    //     h: {
    //         rx: '^[a-zA-Z0-9]([a-zA-Z0-9-.]*[a-zA-Z0-9])?$',
    //         msg: 'can contain letters, digits, dots, and dashes, ' +
    //             'should start and end only with a letter or a digit. e.g. test5.my-domain.home, or test5'
    //     },
    //     nd: {
    //         rx: '^[0-9]+$',
    //         msg: 'can only contain digits'
    //     },
    //     nf: {
    //         rx: '^[0-9.]+$',
    //         msg: 'can only contain digits and decimal separator'
    //     },
    //     p: {
    //         rx: '^[a-zA-Z0-9!@#$%^&*_=+-]{8,}$',
    //         msg: 'should be at least 8 characters long, can contain letters, digits, ! @ # $ % ^ & * _ = + - signs'
    //     }
    // }
    // function updateRangeValue(el) {
    //     const id = '#v-' + el.name;
    //     $(id).textContent = el.value + el.dataset.units;
    // }

    function initAll() {
        // document.querySelectorAll('input[type=number].d').forEach(el => {
        //     el.pattern = patterns.nd.rx;
        //     el.step = 1;
        // });
        // document.querySelectorAll('input[type=number].f').forEach(el => {
        //     el.pattern = patterns.nf.rx;
        //     el.step = 0.1;
        // });
        // // input=password
        // document.querySelectorAll('input.p').forEach(el => {
        //     el.pattern = patterns.p.rx;
        //     el.title = patterns.p.msg;
        //     el.type = 'password';
        // });
        // // input=text
        // document.querySelectorAll('input.t').forEach(el => {
        //     el.type = 'text';
        // });
        // // pattern for ip address
        // document.querySelectorAll('input.t.a').forEach(el => {
        //     el.pattern = patterns.a.rx;
        //     el.title = patterns.a.msg;
        // });
        // // pattern for hostname
        // document.querySelectorAll('input.t.h').forEach(el => {
        //     el.pattern = patterns.h.rx;
        //     el.title = patterns.h.msg;
        // });
        // range
        // $$('input[type=range]').forEach(el => {
        //     el.addEventListener('input', ev => {
        //         updateRangeValue(ev.target);
        //     });
        //     updateRangeValue(el);
        // });

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
    }

    window.onload = initAll;
})();
