#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleCron"
%>
<%in _header.cgi %>
<% ex "cat /etc/crontabs/root" %>
<%in _footer.cgi %>
