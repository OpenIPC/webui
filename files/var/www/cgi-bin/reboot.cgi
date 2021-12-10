#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="Rebooting..."
command="reboot -d 3"
output=$(reboot -d 3)
result=$?
if [ "0" -ne "$result" ]; then %>
<%in _header.cgi %>
<% report_command_error "$command"  "output" %>
<%in _footer.cgi %>
<% else
  redirect_to "/cgi-bin/progress.cgi"
fi
%>
