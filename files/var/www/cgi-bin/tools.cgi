#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="$t_tools_0"
tOptions_tools_interface="auto ${interfaces}"
tools_action="${POST_tools_action:=ping}"
tools_target="${POST_tools_target:=4.2.2.1}"
tools_interface="${POST_tools_interface:=auto}"
tools_packet_size="${POST_tools_packet_size:=56}" # 56-1500 for ping, 38-32768 for trace
tools_duration="${POST_tools_duration:=5}"
%>
<%in p/header.cgi %>
<div class="row g-4">
<div class="col col-md-4 col-lg-3">
<h3><%= $t_tools_1 %></h3>
<form action="/cgi-bin/tools.cgi" method="post">
<%
field_select "tools_action"
field_text "tools_target" "data-pattern=pat-host-ip required"
field_select "tools_interface" "data-pattern=pat-host-ip required"
field_number "tools_packet_size"
field_number "tools_duration" "min=1 max=30 step=1"
button_submit "$t_tools_2"
%>
</form>
</div>
<div class="col col-md-8 col-lg-9">
<%
if [ "POST" = "$REQUEST_METHOD" ]; then
  case "$tools_action" in
    ping)
      title=$t_tools_3
      cmd="ping"
      [ "auto" != "$tools_interface" ] && cmd="$cmd -I $tools_interface"
      cmd="$cmd -s $tools_packet_size"
      cmd="$cmd -c $tools_duration"
      cmd="$cmd $tools_target"
      ;;
    trace)
      title=$t_tools_4
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
%>
<h3><%= $title %></h3>
<h6># <%= $cmd %></h6>
<pre id="output" data-cmd="<%= $cmd %>"></pre>
<% fi %>
</div>
</div>
<%in p/footer.cgi %>
