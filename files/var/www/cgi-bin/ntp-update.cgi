#!/usr/bin/haserl
<%in _common.cgi %>
<%
command="/usr/sbin/ntpd -q -d -n"
output=$(/usr/sbin/ntpd -q -d -n 2>&1)
result=$?
if [ "0" -ne "$result" ]; then %>
<%in _header.cgi %>
<% report_command_error "$command" "$output" %>
<%in _footer.cgi %>
<% else
  redirect_to "/cgi-bin/status.cgi"
fi
%>
