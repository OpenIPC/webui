#!/usr/bin/haserl
<%in _common.cgi %>
<%
command="cp /rom/etc/ntp.conf /etc/ntp.conf"
output=$(cp /rom/etc/ntp.conf /etc/ntp.conf 2>&1)
if [ $? -ne 0 ]; then %>
<%in _header.cgi %>
<% report_command_error "$command" "$output" %>
<%in _footer.cgi %>
<% else
  redirect_to "/cgi-bin/network-ntp.cgi"
fi
%>
