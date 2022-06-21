#!/usr/bin/haserl
<%in _common.cgi %>
<%
_c="cp /rom/etc/ntp.conf /etc/ntp.conf"
_o=$($_c 2>&1)
if [ $? -ne 0 ]; then %>
<%in _header.cgi %>
<% report_command_error "$_c" "$_o" %>
<%in p/footer.cgi %>
<% else
redirect_to "/cgi-bin/network-ntp.cgi"
fi
%>
