#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleFirmwareUpdate"
%>
<%in _header.cgi %>
<%
if [ -f /tmp/webjob.lock ]; then
  report_error "danger" "$tMsgAnotherProcessRunning"
else
  opts=""
  [ "$POST_fw_kernel" = "true" ] && opts="${opts} -k"
  [ "$POST_fw_rootfs" = "true" ] && opts="${opts} -r"
  [ "$POST_fw_reset" = "true" ] && opts="${opts} -n"
  [ "$POST_fw_noreboot" = "true" ] && opts="${opts} -x"
  [ "$POST_fw_enforce" = "true" ] && opts="${opts} --force_ver"
  echo "<pre class=\"bg-light p-4 log-scroll\">"
  echo "sysupgrade ${opts}"
  sysupgrade ${opts} 2>&1
  echo "</pre>"
  button_home
fi
%>
<%in _footer.cgi %>
