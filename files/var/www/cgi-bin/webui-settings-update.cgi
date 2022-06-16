#!/usr/bin/haserl
<%in _common.cgi %>
<%
locale="${POST_webui_language:=en}"
echo "$locale" > /etc/web_locale
reload_locale

default_password=$(grep admin /rom/etc/httpd.conf | cut -d: -f3)
old_password=$(grep admin /etc/httpd.conf | cut -d: -f3)
new_password="$POST_webui_password"
new_password_confirmation="$POST_webui_password_confirmation"

if [ -z "$new_password" ] && [ "$default_password" != "$old_password" ]; then
  flash_save "success" "$tMsgChangesSaved"
  redirect_to "/cgi-bin/webui-settings.cgi"
  exit
elif [ -n "$(echo "$new_password" | grep " ")" ]; then
  flash_save "danger" "$tMsgPasswordHasSpaces"
  redirect_to "/cgi-bin/webui-settings.cgi"
  exit
elif [ "5" -ge "${#new_password}" ]; then
  flash_save "danger" "$tMsgPasswordIsTooShort"
  redirect_to "/cgi-bin/webui-settings.cgi"
  exit
elif [ -z "$new_password_confirmation" ]; then
  flash_save "danger" "$tMsgPasswordNeedsConfirmation"
  redirect_to "/cgi-bin/webui-settings.cgi"
  exit
elif [ "$new_password" != "$new_password_confirmation" ]; then
  flash_save "danger" "$tMsgPasswordDosntMatch"
  redirect_to "/cgi-bin/webui-settings.cgi"
  exit
fi

result=$(sed -i s/:admin:.*/:admin:${new_password}/ /etc/httpd.conf 2>&1)
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
