#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleLog"
%>
<%in _header.cgi %>
<%
ex "/sbin/logread"
button_refresh
%>
<%in _footer.cgi %>
