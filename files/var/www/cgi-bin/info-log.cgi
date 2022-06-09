#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleLog"
%>
<%in _header.cgi %>
<%
b "# logread"
report_log "$(logread | tail -100)"
button_refresh
%>
<%in _footer.cgi %>
