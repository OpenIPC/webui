#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="$t_dmesg_0" %>
<%in p/header.cgi %>
<%
ex "/bin/dmesg"
button_refresh
%>
<%in p/footer.cgi %>
