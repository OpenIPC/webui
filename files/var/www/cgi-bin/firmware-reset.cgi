#!/usr/bin/haserl
<%in _common.cgi %>
<%
command="/usr/sbin/firstboot -s"
output=$(/usr/sbin/firstboot -s 2>&1)
result=$?
if [ "0" -ne "$result" ]; then %>
<%in _header.cgi %>
<% report_command_error "$command" "$output" %>
<%in _footer.cgi %>
<% else
  redirect_to "/cgi-bin/firmware.cgi"
fi
%>
