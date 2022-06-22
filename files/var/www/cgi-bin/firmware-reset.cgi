#!/usr/bin/haserl
<%in _common.cgi %>
<% page_title="$t_fwreset_0" %>
<%in _header.cgi %>
<%
pre_ "bg-light p-4 log-scroll"
  sysupgrade -n
_pre
button_home
button_reboot
%>
<%in p/footer.cgi %>
