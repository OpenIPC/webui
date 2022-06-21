#!/usr/bin/haserl
<%in _common.cgi %>
<% page_title="$t_log_0" %>
<%in _header.cgi %>
<%
ex "/sbin/logread"
button_refresh
%>
<%in p/footer.cgi %>
