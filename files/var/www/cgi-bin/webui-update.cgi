#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Updating Web UI"
c="/usr/sbin/updatewebui.sh"
reboot="true"
[ "true" = "$POST_web_enforce" ] && c="${c} -f"
[ "true" = "$POST_web_verbose" ] && c="${c} -v"
[ "true" = "$POST_web_noreboot" ] && reboot="false"
c="${c} -b $POST_web_version"
%>
<%in p/header.cgi %>
<h3 class="alert alert-warning">DO NOT CLOSE, REFRESH, OR NAVIGATE FROM THIS PAGE UNTIL THE PROCESS IS FINISHED!</h3>
<h5># <%= $c %></h5>
<pre id="output" data-cmd="<%= $c %>" data-reboot="<%= $reboot %>"></pre>
<%in p/footer.cgi %>
