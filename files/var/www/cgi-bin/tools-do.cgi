#!/usr/bin/haserl
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
%>
<%in _header.cgi %>
<% if [ "0" -ne "$result" ]; then %>
<h2 class="text-danger">Oops. Something happened.</h2>
<div class="alert alert-danger">
<pre>
<b># <%= $command %></b>
<%= "$output" %>
</pre>
</div>
<% else %>
<h2><%= $title %>. Please wait...</h2>
<div class="alert alert-success">
<pre>
<b># <%= $command %></b>
<%= "$output" %>
</pre>
</div>
<p><a href="/cgi-bin/tools.cgi">Go back to monitoring tools</a></p>
<% fi %>
<%in _footer.cgi %>
