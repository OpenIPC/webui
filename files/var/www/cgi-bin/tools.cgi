#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPT_Tools"
tOptions_tools_interface="auto ${interfaces}"
tools_action="${POST_tools_action:=ping}"
tools_target="${POST_tools_target:=4.2.2.1}"
tools_interface="${POST_tools_interface:=auto}"
tools_packet_size="${POST_tools_packet_size:=56}" # 56-1500 for ping, 38-32768 for trace
tools_duration="${POST_tools_duration:=5}"
%>
<%in _header.cgi %>
<div class="row g-3">
<div class="col-md-6 col-lg-4">
<div class="card mb-3 h-100">
<div class="card-header"><%= $tHD_Ping %></div>
<div class="card-body">
<form action="/cgi-bin/tools.cgi" method="post">
<%
field_select "tools_action"
field_text "tools_target" "data-pattern=pat-host-ip required"
field_select "tools_interface" "data-pattern=pat-host-ip required"
field_number "tools_packet_size"
field_number "tools_duration" "min=1 max=30 step=1"
button_submit "$tB_Run" "primary"
%>
</form>
</div>
</div>
</div>

<%
  if [ "POST" = "$REQUEST_METHOD" ]; then
    case "$tools_action" in
      ping)
        cmd="ping"
        [ "auto" != "$tools_interface" ] && cmd="${cmd} -I ${tools_interface}"
        cmd="${cmd} -s ${tools_packet_size}"
        cmd="${cmd} -c ${tools_duration}"
        cmd="${cmd} ${tools_target}"
        col_card_ "Ping Quality" "col-8 mb-3"
          pre_
            $cmd
          _pre
        _col_card
        ;;
      trace)
        cmd="traceroute"
        # order is important!
        cmd="${cmd} -q ${tools_duration}"
        cmd="${cmd} -w 1"
        [ "auto" != "$tools_interface" ] && cmd="${cmd} -i ${POST_tools_interface}"
        cmd="${cmd} ${tools_target}"
        cmd="${cmd} ${tools_packet_size}"
        col_card "Traceroute Quality" "col-8 mb-3"
          pre
            $cmd
          _pre
        _col_card
        ;;
      *)
        ;;
    esac
  fi
_row
%>
<%in p/footer.cgi %>
