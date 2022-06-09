#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleDmesg"
%>
<%in _header.cgi %>
<%
b "# dmesg"
report_log "$(dmesg)"
button_refresh
%>
<%in _footer.cgi %>
