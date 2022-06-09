#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleCron"
%>
<%in _header.cgi %>
<%
b "# cat /etc/crontabs/root"
report_log "$(cat /etc/crontabs/root)"
%>
<%in _footer.cgi %>
