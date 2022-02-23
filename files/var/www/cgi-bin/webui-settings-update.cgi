#!/usr/bin/haserl
<%in _common.cgi %>
<%
if [ -z "$POST_language" ]; then
  language="en"
else
  language="$POST_language"
fi
echo $language > /etc/web_locale

if [ -z "$POST_password" ] && [ "12345" != "$password" ]; then
  flash_save "success" "$tMsgChangesSaved"
  redirect_to "/cgi-bin/webui-settings.cgi"
  exit
elif [[ ! -z "$(echo "$POST_password" | grep " ")" ]]; then
  flash_save "danger" "$tMsgPasswordHasSpaces"
  redirect_to "/cgi-bin/webui-settings.cgi"
  exit
elif [ "5" -ge "${#POST_password}" ]; then
  flash_save "danger" "$tMsgPasswordIsTooShort"
  redirect_to "/cgi-bin/webui-settings.cgi"
  exit
elif [ -z "$POST_passwordconfirmation" ]; then
  flash_save "danger" "$tMsgPasswordNeedsConfirmation"
  redirect_to "/cgi-bin/webui-settings.cgi"
  exit
elif [ "$POST_password" != "$POST_passwordconfirmation" ]; then
  flash_save "danger" "$tMsgPasswordDosntMatch"
  redirect_to "/cgi-bin/webui-settings.cgi"
  exit
fi

result=$(sed -i s/:admin:.*/:admin:${POST_password}/ /etc/httpd.conf 2>&1)
if [ $? -eq 0 ]; then
  flash_delete
  flash_save "success" "$tMsgChangesSaved"
  redirect_to "/cgi-bin/status.cgi"
else
%>
<%in _header.cgi %>
<% report_command_info "$command" "$result" %>
<%in _footer.cgi %>
<% fi %>
