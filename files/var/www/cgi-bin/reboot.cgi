#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPT_Reboot"
cmd="reboot -d 3"
res="$($cmd)"
if [ $? -ne 0 ]; then
%>
<%in _header.cgi %>
<% report_command_error "$cmd"  "$res" %>
<%in p/footer.cgi %>
<% else
redirect_to "/cgi-bin/progress.cgi"
fi
%>
