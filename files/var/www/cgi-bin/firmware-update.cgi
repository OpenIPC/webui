#!/usr/bin/haserl
<%in _common.cgi %>
<%
if [ -z "$POST_debug" ]; then
  redirect_to "/cgi-bin/progress.cgi"
else %>
<%in _debug.cgi %>
<% fi
opts=""
[ ! -z "$POST_kernel"   ] && opts="${opts} -k"
[ ! -z "$POST_rootfs"   ] && opts="${opts} -r"
[ ! -z "$POST_reset"    ] && opts="${opts} -n"
[ ! -z "$POST_noreboot" ] && opts="${opts} -x"
[ ! -z $(sysupgrade | grep force) ] && opts="${opts} --force"
sysupgrade ${opts} 2>&1
%>
