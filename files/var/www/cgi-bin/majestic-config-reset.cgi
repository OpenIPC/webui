#!/usr/bin/haserl
<%in _common.cgi %>
<%
command="cp -f /rom/etc/majestic.yaml /etc/majestic.yaml"
output=$(cp -f /rom/etc/majestic.yaml /etc/majestic.yaml 2>&1)
if [ $? -ne 0 ]; then %>
<%in _header.cgi %>
<% report_command_error "$command" "$output" %>
<%in _footer.cgi %>
<% else
  redirect_to "/cgi-bin/majestic-config-compare.cgi"
fi
%>
