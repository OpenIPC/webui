#!/usr/bin/haserl
<%in _common.cgi %>
<%
_c="cp -f /rom/etc/majestic.yaml /etc/majestic.yaml"
_o=$($_c 2>&1)
if [ $? -ne 0 ]; then %>
<%in _header.cgi %>
<% report_command_error "$_c" "$_o" %>
<%in p/footer.cgi %>
<% else
redirect_to "/cgi-bin/majestic-config-compare.cgi"
fi
%>
