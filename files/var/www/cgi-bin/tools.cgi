#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_system_info
page_title="$tPageTitleTools"
%>
<%in _header.cgi %>
<%
tOptions_tools_interface="auto,${interfaces}"

tools_action="${POST_tools_action:=ping}"
tools_target="${POST_tools_target:=4.2.2.1}"
tools_interface="${POST_tools_interface:=auto}"
tools_packet_size="${POST_tools_packet_size:=56}" # 56-1500 for ping, 38-32768 for trace
tools_duration="${POST_tools_duration:=5}"

row_ "row-cols-1 row-cols-lg-2 row-cols-xl-3 g-3 mb-3"
  col_card_ "$tHeaderPing"
    form_ "/cgi-bin/tools.cgi" "post"
      field_select "tools_action"
      field_text "tools_target" "data-pattern=\"pat-host-ip\" required"
      field_select "tools_interface" "data-pattern=\"pat-host-ip\" required"
      field_number "tools_packet_size"
      field_number "tools_duration" "min=1 max=30 step=1"
      button_submit "$tButtonRun" "primary"
    _form
  _col_card

  if [ "POST" = "$REQUEST_METHOD" ]; then
    case "$tools_action" in
      ping)
        cmd="ping"
        [ "auto" != "$tools_interface" ] && cmd="${cmd} -I ${tools_interface}"
        cmd="${cmd} -s ${tools_packet_size}"
        cmd="${cmd} -c ${tools_duration}"
        cmd="${cmd} ${tools_target}"
        col_card "Ping Quality" "$(ex "$cmd")"
        ;;
      trace)
        cmd="traceroute"
        # order is important!
        cmd="${cmd} -q ${tools_duration}"
        cmd="${cmd} -w 1"
        [ "auto" != "$tools_interface" ] && cmd="${cmd} -i ${POST_tools_interface}"
        cmd="${cmd} ${tools_target}"
        cmd="${cmd} ${tools_packet_size}"
        col_card "Traceroute Quality" "$(ex "$cmd")"
        ;;
      *)
        ;;
    esac
  fi
_row
%>
<%in _footer.cgi %>
