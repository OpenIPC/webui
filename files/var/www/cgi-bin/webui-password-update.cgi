#!/usr/bin/haserl
<%in _common.cgi %>
<%
password="$POST_password"
confirmation="$POST_passwordconfirmation"
if [ -z "$password" ]; then
  flash_save "danger" "Password cannot be empty!"
  redirect_to "/cgi-bin/webui-password.cgi"
  exit
elif [[ ! -z "$(echo "$password" | grep " ")" ]]; then
  flash_save "danger" "Password cannot have spaces!"
  redirect_to "/cgi-bin/webui-password.cgi"
  exit
elif [ "5" -ge "${#password}" ]; then
  flash_save "danger" "Password cannot be shorter than 6 characters!"
  redirect_to "/cgi-bin/webui-password.cgi"
  exit
elif [ -z "$confirmation" ]; then
  flash_save "danger" "Password requires confirmation!"
  redirect_to "/cgi-bin/webui-password.cgi"
  exit
elif [ "$password" != "$confirmation" ]; then
  flash_save "danger" "Password does not match its confirmation!"
  redirect_to "/cgi-bin/webui-password.cgi"
  exit
fi

command="sed -i s/:admin:.*/:admin:${password}/ /etc/httpd.conf"
result=$(sed -i s/:admin:.*/:admin:${password}/ /etc/httpd.conf 2>&1)
[ -z "$result" ] && flash_delete

if [ -z "$DEBUG" ]; then
  flash_save "success" "Password updated."
  redirect_to "/cgi-bin/status.cgi"
else
%>
<%in _header.cgi %>
<% report_command_info "$command" "$result" %>
<%in _footer.cgi %>
<% fi %>