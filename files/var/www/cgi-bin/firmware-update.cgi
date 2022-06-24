#!/usr/bin/haserl
<%in p/common.cgi %>
<%
check_for_lock
page_title="$t_fwupdate_0"
opts=""
[ "$POST_fw_kernel" = "true" ] && opts="${opts} -k"
[ "$POST_fw_rootfs" = "true" ] && opts="${opts} -r"
[ "$POST_fw_reset" = "true" ] && opts="${opts} -n"
[ "$POST_fw_noreboot" = "true" ] && opts="${opts} -x"
[ "$POST_fw_enforce" = "true" ] && opts="${opts} --force_ver"
cmd="sysupgrade $opts"
%>
<%in p/header.cgi %>
<h6># <%= $cmd %></h6>
<pre id="output" data-cmd="<%= $cmd %>" data-reboot="true"></pre>
<%in p/footer.cgi %>
