#!/usr/bin/haserl
<%in _common.cgi %>
<%
case $FORM_action in
  ping)
    [ "auto" = "$FORM_iface" ] && iface="" || iface=" -I $FORM_iface"
    command="ping -c 15 -s 1500 ${iface}${FORM_target}"
    title="Ping Quality"
    ;;
  trace)
    [ "auto" = "$FORM_iface" ] && iface="" || iface=" -i $FORM_iface"
    command="traceroute ${iface}${FORM_target}"
    title="Traceroute Quality"
    ;;
esac

output=$($command 2>&1)
result=$?

if [ "0" -eq "$result" ]; then
%>
<%in _header.cgi %>
<%
  report_command_success "$command" "$output"
else
  report_command_error "$command" "$output"
fi
%>
<p><a href="/cgi-bin/tools.cgi">Go back to monitoring tools</a></p>
<%in _footer.cgi %>
