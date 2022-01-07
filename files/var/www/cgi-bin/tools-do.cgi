#!/usr/bin/haserl
<%in _common.cgi %>
<%
opts=""
case $POST_action in
  ping)
    title="Ping Quality"
    [ -n "$POST_size" ] && opts="${opts} -s ${POST_size}"
    [ -n "$POST_duration" ] && opts="${opts} -c ${POST_duration}"
    [ "auto" != "$POST_iface" ] && opts="${opts} -I ${POST_iface}"
    opts="${opts} ${POST_target}"
    command="ping ${opts}"
    output=$(ping ${opts} 2>&1)
    ;;
  trace)
    title="Traceroute Quality"
    [ "auto" != "$POST_iface" ] opts="${opts]} -i ${POST_iface}"
    [ -n "$POST_duration" ] && opts="${opts} -q ${POST_duration}"
    opts="${opts} ${POST_target}"
    [ -n "$POST_size" ] && opts="${opts} ${POST_size}"
    command="traceroute ${opts}"
    output=$(traceroute ${opts} 2>&1)
    ;;
esac
%>
<%in _header.cgi %>
<%
if [ $? -eq 0 ]; then
  report_command_success "$command" "$output"
else
  report_command_error "$command" "$output"
fi
%>
<p><a href="/cgi-bin/tools.cgi">Go back to monitoring tools</a></p>
<%in _footer.cgi %>
