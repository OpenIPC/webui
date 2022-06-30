#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Monitoring tools"
tools_action="${POST_tools_action:=ping}"
tools_target="${POST_tools_target:=4.2.2.1}"
tools_interface="${POST_tools_interface:=auto}"
tools_packet_size="${POST_tools_packet_size:=56}" # 56-1500 for ping, 38-32768 for trace
tools_duration="${POST_tools_duration:=5}"

if [ "POST" = "$REQUEST_METHOD" ]; then
  case "$tools_action" in
    ping)
      title="Ping Quality"
      cmd="ping"
      [ "auto" != "$tools_interface" ] && cmd="$cmd -I $tools_interface"
      cmd="$cmd -s $tools_packet_size"
      cmd="$cmd -c $tools_duration"
      cmd="$cmd $tools_target"
      ;;
    trace)
      title="Traceroute Quality"
      cmd="traceroute"
      # order is important!
      cmd="$cmd -q $tools_duration"
      cmd="$cmd -w 1"
      [ "auto" != "$tools_interface" ] && cmd="$cmd -i $tools_interface"
      cmd="$cmd $tools_target"
      cmd="$cmd $tools_packet_size"
      ;;
    *)
      ;;
  esac
fi
%>
<%in p/header.cgi %>

<div class="row g-4">
  <div class="col col-md-4 col-lg-3">
    <h3>Ping Quality</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_select "tools_action" "Action" "ping,trace" %>
      <% field_text "tools_target" "Target FQDN or IP address" %>
      <% field_select "tools_interface" "Network interface" "auto,${interfaces}" %>
      <% field_number "tools_packet_size" "Packet size" "56,65535,1" "Bytes" %>
      <% field_number "tools_duration" "Number of packets" "1,30,1" %>
      <% button_submit "Run" %>
    </form>
  </div>
  <div class="col col-md-8 col-lg-9">
    <h3><%= $title %></h3>
    <h4># <%= $cmd %></h4>
  <% if [ -n "$cmd" ]; then %>
    <pre id="output" data-cmd="<%= $cmd %>"></pre>
  <% fi %>
  </div>
</div>

<%in p/footer.cgi %>
