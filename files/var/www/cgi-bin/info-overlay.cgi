#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleOverlay"
%>
<%in _header.cgi %>
<%
b "# ls -Rl /overlay"
report_log "$(ls -Rl /overlay)"
%>
<%in parts/reset-firmware.cgi %>
<%in _footer.cgi %>
