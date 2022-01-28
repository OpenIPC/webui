#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleFirmwareReset"
%>
<%in _header.cgi %>
<%
command="/usr/sbin/firstboot -s"
output=$(/usr/sbin/firstboot -s 2>&1)
if [ $? -ne 0 ]; then
  report_command_error "$command" "$output"
else
  report_command_info "$command" "$output"
%>
<a class="btn btn-primary" href="/"><%= $tButtonGoHome %></a>
<% fi %>
<%in _footer.cgi %>
