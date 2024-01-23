#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Erasing overlay"
c="/usr/sbin/sysupgrade.sh -n"
reboot="true"
%>
<%in p/header.cgi %>
<pre id="output" data-cmd="<%= $c %>" data-reboot="<%= $reboot %>"></pre>
<a class="btn btn-primary" href="/">Go home</a>
<a class="btn btn-danger" href="reboot.cgi">Reboot camera</a>
<%in p/footer.cgi %>
