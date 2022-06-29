#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Updating Web UI"
c="/usr/sbin/updatewebui.sh"
[ "true" = "$POST_web_enforce" ] && c="${c} -f"
c="${c} -b $POST_web_version"
%>
<%in p/header.cgi %>
<h4># <%= $c %></h4>
<pre id="output" data-cmd="<%= $c %>" data-reboot="false"></pre>
<%in p/footer.cgi %>
