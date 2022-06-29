#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="HTTPd" %>
<%in p/header.cgi %>
<h3>HTTPd config</h3>
<% ex "cat /etc/httpd.conf" %>
<h3>HTTPd environment</h3>
<% ex "/bin/printenv" %>
<%in p/footer.cgi %>
