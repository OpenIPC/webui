#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="$t_log_0" %>
<%in p/header.cgi %>
<%
ex "/sbin/logread"
button_refresh
%>
<%in p/footer.cgi %>
