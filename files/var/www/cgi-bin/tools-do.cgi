#!/usr/bin/haserl
content-type: text/html

<%in _header.cgi %>
<%
case $FORM_action in
  ping)
    echo "<h2>Ping Quality. Please wait...</h2>"
    echo "<div class=\"alert alert-success\">"
    echo -n "<pre>" 
    if [ "$FORM_iface" = "auto" ]; then
      echo "<b># ping -c 15 -s 1500 ${FORM_target}</b><br>"
      echo "$(ping -c 15 -s 1500 ${FORM_target} 2>&1)"
    else
      echo "<b># ping -c 15 -s 1500 -I ${FORM_iface} ${FORM_target}</b><br>"
      echo "$(ping -c 15 -s 1500 -I ${FORM_iface} ${FORM_target} 2>&1)"
    fi
    echo "</pre>"
    echo "</div>"
    ;;
  trace)
    echo "<h2>Trace Route. Please wait...</h2>"
    echo "<div class=\"alert alert-success\">"
    echo -n "<pre>"
    if [ "$FORM_iface" = "auto" ]; then
      echo "<b># traceroute $FORM_target</b><br>"
      echo "$(traceroute $FORM_target 2>&1)"
    else
      echo "<b># traceroute -i $FORM_iface $FORM_target</b><br>"
      echo "$(traceroute -i $FORM_iface $FORM_target 2>&1)"
    fi
    echo "</pre>"
    echo "</div>"
    ;;
esac
%>
<p><a href="/cgi-bin/tools.cgi">Go back to monitoring tools</a></p>
<%in _footer.cgi %>
