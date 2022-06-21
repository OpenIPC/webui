#!/usr/bin/haserl --upload-limit=100 --upload-dir=/tmp
<%in _common.cgi %>
<%
if [ "POST" = "$REQUEST_METHOD" ]; then
  # language routine
  locale="$POST_webui_language" # set language.
  # upload new language and switch to it. overrides aboveset language.
  _fname="$POST_webui_locale_file_name"
  if [ -n "$_fname" ]; then
    mv "$POST_webui_locale_file_path" /var/www/lang/$_fname
    locale=${_fname%%.*}
  fi
  # save new language settings and reload locale
  [ -z "$locale" ] && locale="en"
  echo "$locale" > /etc/web_locale
  reload_locale

  # password routine
  new_password="$POST_webui_password"
  new_password_confirmation="$POST_webui_password_confirmation"

  if [ -z "$new_password" ]; then
    error="$tMsgPasswordCannotBeEmpty"
  elif [ "$password_fw" = "$new_password" ]; then
    error="$tMsgPasswordIsDefault"
  elif [ -n "$(echo "$new_password" | grep " ")" ]; then
    error="$tMsgPasswordHasSpaces"
  elif [ "5" -ge "${#new_password}" ]; then
    error="$tMsgPasswordIsTooShort"
  elif [ -z "$new_password_confirmation" ]; then
    error="$tMsgPasswordNeedsConfirmation"
  elif [ "$new_password" != "$new_password_confirmation" ]; then
    error="$tMsgPasswordsDontMatch"
  fi

  if [ -z "$error" ]; then
    sed -i s/:admin:.*/:admin:${new_password}/ /etc/httpd.conf
    redirect_to $SCRIPT_NAME "success" "Changes saved."
  fi
fi

page_title="$tPT_WebuiSettings"
tOptions_webui_language="en|English"
for i in /var/www/lang/; do
  code="$(basename $i)"; code="${code%%.sh}"
  name="$(sed -n 2p $i|sed "s/ /_/g"|cut -d: -f2)"
  tOptions_webui_language="${tOptions_webui_language},${code}|${name}"
done

# data for form fields
webui_username="admin"
webui_language="$locale"
%>
<%in _header.cgi %>
<%
[ -n "$error" ] && report_error "$error"

form_upload_ "/cgi-bin/webui-settings.cgi"
  row_
    col_ "col-md-6 col-xl-4"
      card_ "$tHD_WebuiAccess"
        field_text "webui_username" "" "autocomplete=\"username\" disabled"
        field_password "webui_password" "" "autocomplete=\"new-password\""
        field_password "webui_password_confirmation" "autocomplete=\"new-password\""
      _card
    _col
    col_ "col-md-6 col-xl-4"
      card_ "$tHD_WebuiLocale"
        field_select "webui_language"
        field_file "webui_locale_file"
      _card
    _col
    col_ "col-md-6 col-xl-4"
      card_ "$tHD_WebuiConfig"
        ex "cat /etc/httpd.conf"
        ex "echo \$locale"
        ex "cat /etc/web_locale"
        ex "ls /var/www/lang/"
      _card
    _col
  _row
  button_submit "$t_btn_submit" "primary"
_form
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
</script>
<%in p/footer.cgi %>
