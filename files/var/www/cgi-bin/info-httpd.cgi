#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleHttpdEnv"
%>
<%in _header.cgi %>
<%
b "# printenv"
report_log "$(printenv | sort)"
%>
<%in _footer.cgi %>
