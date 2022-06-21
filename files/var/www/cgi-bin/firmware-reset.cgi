#!/usr/bin/haserl
<%in _common.cgi %>
<% page_title="$t_fwreset_0" %>
<%in _header.cgi %>
<%
_c="/usr/sbin/sysupgrade -n"
_o=$($_c 2>&1)
if [ $? -ne 0 ]; then
report_command_error "$_c" "$_o"
else
report_command_info "$_c" "$_o"
button_home
fi
%>
<%in p/footer.cgi %>
