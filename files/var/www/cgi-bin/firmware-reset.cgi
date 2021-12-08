#!/usr/bin/haserl
<%
command="/usr/sbin/firstboot -s"
output=$(/usr/sbin/firstboot -s 2>&1)
result=$?
if [ "0" -ne "$result" ]; then %>
<%in _header.cgi %>
<% report_command_error "$command" "$output" %>
<%in _footer.cgi %>
<% else
  redirect_to "/cgi-bin/updates.cgi"
fi
%>
