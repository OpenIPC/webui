#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$t_reboot_0"
_c="reboot -d 3"
_o="$($cmd)"
if [ $? -ne 0 ]; then
%>
<%in _header.cgi %>
<% report_command_error "$_c"  "$_o" %>
<%in p/footer.cgi %>
<% else
redirect_to "/cgi-bin/progress.cgi"
fi
%>
