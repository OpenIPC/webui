#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Upgrading firmware"
c="/usr/sbin/sysupgrade"
reboot="true"
[ "true" = "$POST_fw_kernel" ] && c="${c} -k"
[ "true" = "$POST_fw_rootfs" ] && c="${c} -r"
[ "true" = "$POST_fw_reset" ] && c="${c} -n"
[ "true" = "$POST_fw_noreboot" ] && c="${c} -x" && reboot="false"
[ "true" = "$POST_fw_enforce" ] && c="${c} --force_ver"
%>
<%in p/header.cgi %>
<h5># <%= $c %></h5>
<pre id="output" data-cmd="<%= $c %>" data-reboot="<%= $reboot %>"></pre>
<%in p/footer.cgi %>
