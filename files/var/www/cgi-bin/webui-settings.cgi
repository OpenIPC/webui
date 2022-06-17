#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleWebuiSettings"
%>
<%in _header.cgi %>
<%
tOptions_webui_language=""
for i in locale/*.sh; do
  code="$(echo $i | sed 's#^locale/\(.*\)\.sh#\1#')"
  name="$(sed -n 2p $i | cut -d: -f2)"
  tOptions_webui_language="${tOptions_webui_language},${code}|${name}"
done

webui_username="admin"
webui_language="$locale"

row_
  col_ "col-md-6 col-xl-4"
    card_ "$tHeaderWebuiSettings"
      form_ "/cgi-bin/webui-settings-update.cgi" "post"
        field_text "webui_username" "autocomplete=\"username\" disabled"
        field_password "webui_password" "autocomplete=\"new-password\""
        field_password "webui_password_confirmation" "autocomplete=\"new-password\""
        field_select "webui_language"
        button_submit "$tButtonFormSubmit" "primary"
      _form
    _card
  _col
_row
%>

<script>
$$('.toggle-password').forEach(el => {
  el.addEventListener('click', (ev) => {
    const type = (ev.target.checked) ? 'type' : 'password';
    $$('input.password').forEach(el => el.type = type);
    $$('.toggle-password').forEach(el => el.checked = ev.target.checked);
    $('#password').focus();
  })
});
<% if [ -z "$webui_language" ]; then %>
$('#webui_language').value = (window.navigator.language.startsWith('ru')) ? 'ru' : 'en';
<% fi %>
</script>
<%in _footer.cgi %>
