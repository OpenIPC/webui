#!/usr/bin/haserl
<%in _common.cgi %>
<%
_c="/usr/sbin/ntpd -q -d -n"
_o=$($_c 2>&1)
if [ $? -ne 0 ]; then
%>
<%in _header.cgi %>
<% report_command_error "$_c" "$_o" %>
<%in p/footer.cgi %>
<%
else
flash_save "success" "$t_ntp_a"
redirect_to "/cgi-bin/status.cgi"
fi
%>
