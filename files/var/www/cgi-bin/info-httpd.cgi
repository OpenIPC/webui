#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="$t_httpd_0" %>
<%in p/header.cgi %>
<h3><%= $t_httpd_1 %></h3>
<% ex "cat /etc/httpd.conf" %>
<h3><%= $t_httpd_2 %></h3>
<% ex "/bin/printenv" %>
<%in p/footer.cgi %>
