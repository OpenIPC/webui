#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleDmesg"
%>
<%in _header.cgi %>
<%
ex "/bin/dmesg"
button_refresh
%>
<%in _footer.cgi %>
