$$('.toggle-password').forEach(el => {
  el.addEventListener('click', (ev) => {
    const type = (ev.target.checked) ? 'type' : 'password';
    $$('input.password').forEach(el => el.type = type);
    $$('.toggle-password').forEach(el => el.checked = ev.target.checked);
    $('#password').focus();
  })
});
