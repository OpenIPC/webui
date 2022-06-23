#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="$t_fwupdate_0" %>
<%in p/header.cgi %>
<%
if [ -f /tmp/webjob.lock ]; then
  report_error "danger" "$t_fwupdate_1"
else
  opts=""
  [ "$POST_fw_kernel" = "true" ] && opts="${opts} -k"
  [ "$POST_fw_rootfs" = "true" ] && opts="${opts} -r"
  [ "$POST_fw_reset" = "true" ] && opts="${opts} -n"
  [ "$POST_fw_noreboot" = "true" ] && opts="${opts} -x"
  [ "$POST_fw_enforce" = "true" ] && opts="${opts} --force_ver"

  pre_ "bg-light p-4 log-scroll"
    sysupgrade $opts
  _pre
  button_home
  button_reboot
fi
%>
<%in p/footer.cgi %>
