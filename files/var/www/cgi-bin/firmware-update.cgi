#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="Upgrading Firmware"
%>
<%in _header.cgi %>
<%
if [ -f /tmp/webjob.lock ]; then
  report_error "danger" "Another progress is running."
else
%>
<pre class="bg-light p-4 log-scroll">
<%
  opts=""
  [ ! -z "$POST_kernel"   ] && opts="${opts} -k"
  [ ! -z "$POST_rootfs"   ] && opts="${opts} -r"
  [ ! -z "$POST_reset"    ] && opts="${opts} -n"
  [ ! -z "$POST_noreboot" ] && opts="${opts} -x"
  [ ! -z $(sysupgrade | grep force) ] && opts="${opts} --force"
  echo "sysupgrade ${opts}"
  sysupgrade ${opts} 2>&1
%>
</pre>
<a class="btn btn-primary" href="/">Go Home</a>
<% fi %>
<%in _footer.cgi %>
