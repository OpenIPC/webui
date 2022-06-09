#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleHttpdConfig"
%>
<%in _header.cgi %>
<%
b "# cat /etc/httpd.conf"
report_log "$(cat /etc/httpd.conf)"
%>
<%in _footer.cgi %>
