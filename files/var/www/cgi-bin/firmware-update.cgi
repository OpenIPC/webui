#!/usr/bin/haserl
<%in _common.cgi %>
<%
if [ -z "$FORM_debug" ]; then
  redirect_to "/cgi-bin/progress.cgi"
else
  echo "content-type: text/plain"
  echo ""
fi

opts=""
[ ! -z "$FORM_kernel"  ] && opts="${opts} -k"
[ ! -z "$FORM_rootfs"  ] && opts="${opts} -r"
[ ! -z "$FORM_reset"   ] && opts="${opts} -n"
[ ! -z "$FORM_noreboot"] && opts="${opts} -x"
sysupgrade ${opts}
%>
