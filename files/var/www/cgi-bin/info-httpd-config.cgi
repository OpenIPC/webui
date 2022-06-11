#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleHttpdConfig"
%>
<%in _header.cgi %>
<% ex "cat /etc/httpd.conf" %>
<%in _footer.cgi %>
