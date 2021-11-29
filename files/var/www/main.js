(function(){
    const patterns = {
        a: {
            rx: '^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
            msg: 'IPv4 address consists of four decimal numbers, each ranging from 0 to 255, separated by dots'
        },
        h: {
            rx: '^[a-zA-Z0-9]([a-zA-Z0-9-.]*[a-zA-Z0-9])?$',
            msg: 'can contain letters, digits, dots, and dashes, ' +
                 'should start and end only with a letter or a digit. e.g. test5.my-domain.home, or test5'
        },
        n: {
            rx: '^[0-9]+$',
            msg: 'can only contain digits'
        },
        nf: {
            rx: '^[0-9.]+$',
        },
        p: {
            rx: '^[a-zA-Z0-9!@#$%^&*_=+-]{8,}$',
            msg: 'should be at least 8 characters long, can contain letters, digits, ! @ # $ % ^ & * _ = + - signs'
        }
    }

    function initAll() {
        // input=number
        document.querySelectorAll('input.n').forEach(el => {
            el.min = 0;
            el.pattern = patterns.n.rx;
            el.step = 1;
            el.type = 'number';
        });
        document.querySelectorAll('input.n.f').forEach(el => {
            el.pattern = patterns.nf.rx;
            el.step = 0.1;
        });
        // input=password
        document.querySelectorAll('input.p').forEach(el => {
            el.pattern = patterns.p.rx;
            el.title = patterns.p.msg;
            el.type = 'password';
        });
        // input=text
        document.querySelectorAll('input.t').forEach(el => {
            el.type = 'text';
        });
        // pattern for ip address
        document.querySelectorAll('input.t.a').forEach(el => {
            el.pattern = patterns.a.rx;
            el.title = patterns.a.msg;
        });
        // pattern for hostname
        document.querySelectorAll('input.t.h').forEach(el => {
            el.pattern = patterns.h.rx;
            el.title = patterns.h.msg;
        });
        // select
        document.querySelectorAll('select').forEach(el => {
            el.autocomplete = 'off';
        });

        document.querySelectorAll('a.confirm').forEach(el => {
            el.addEventListener('click', function(event) {
                if (!confirm("Do you want to reboot the device ?"))
                    event.preventDefault();
            });
        });
    }

    window.onload = initAll;
})();
