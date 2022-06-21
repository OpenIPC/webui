#!/usr/bin/haserl
<%in _common.cgi %>
<% page_title="$t_dmesg_0" %>
<%in _header.cgi %>
<%
ex "/bin/dmesg"
button_refresh
%>
<%in p/footer.cgi %>
