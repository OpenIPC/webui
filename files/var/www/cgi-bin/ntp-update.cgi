#!/usr/bin/haserl
<%in p/common.cgi %>
<%
_c="/usr/sbin/ntpd -q -d -n"
_o=$($_c 2>&1)
if [ $? -ne 0 ]; then
%>
<%in p/header.cgi %>
<% report_command_error "$_c" "$_o" %>
<%in p/footer.cgi %>
<%
else
  redirect_to "status.cgi" "success" "Camera time synchronized with NTP server."
fi
%>
