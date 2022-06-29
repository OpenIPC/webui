#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Upgrading firmware"
c="/usr/sbin/sysupgrade"
[ "true" = "$POST_fw_kernel" ] && c="${c} -k"
[ "true" = "$POST_fw_rootfs" ] && c="${c} -r"
[ "true" = "$POST_fw_reset"  ] && c="${c} -n"
[ "true" = "$POST_fw_noreboot" ] && c="${c} -x"
[ "true" = "$POST_fw_enforce"  ] && c="${c} --force_ver"
%>
<%in p/header.cgi %>
<h4># <%= $c %></h4>
<pre id="output" data-cmd="<%= $c %>" data-reboot="true"></pre>
<%in p/footer.cgi %>
