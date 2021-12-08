#!/usr/bin/haserl
<%in _common.cgi %>
<%
case $FORM_action in
  ping)
    [ "auto" = "$FORM_iface" ] && iface="" || iface=" -I $FORM_iface"
    title="Ping Quality"
    command="ping -c 15 -s 1500 ${iface}${FORM_target}"
    output=$(ping -c 15 -s 1500 ${iface}${FORM_target} 2>&1)
    ;;
  trace)
    [ "auto" = "$FORM_iface" ] && iface="" || iface=" -i $FORM_iface"
    title="Traceroute Quality"
    command="traceroute ${iface}${FORM_target}"
    output=$(traceroute ${iface}${FORM_target} 2>&1)
    ;;
esac
result=$?
%>
<%in _header.cgi %>
<%
if [ "0" -eq "$result" ]; then
  report_command_success "$command" "$output"
else
  report_command_error "$command" "$output"
fi
%>
<p><a href="/cgi-bin/tools.cgi">Go back to monitoring tools</a></p>
<%in _footer.cgi %>
