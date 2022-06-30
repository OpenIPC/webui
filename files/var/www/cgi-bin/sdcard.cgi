#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="$t_sdcard_0" %>
<%in p/header.cgi %>
<%
ls /dev/mmc* >/dev/null 2>&1
if [ $? -ne 0 ]; then
%>
<div class="alert alert-danger">
  <h4><%= $t_sdcard_1 %></h4>
  <p><%= $t_sdcard_2 %></p>
</div>
<%
else
  card_device="/dev/mmcblk0"
  card_partition="${card_device}p1"
  mount_point="${card_partition//dev/mnt}"
  error=""
  _o=""
  if [ -n "$POST_doFormatCard" ]; then
%>
<div class="alert alert-danger">
  <h4><%= $t_sdcard_3 %></h4>
  <p><%= $t_sdcard_4 %></p>
</div>
<%
    if [ "$(grep $card_partition /etc/mtab)" ]; then
      _c="umount $card_partition"
      _o="${_o}\n${_c}\n$($_c 2>&1)"
      [ $? -ne 0 ] && error="$t_sdcard_5"
    fi

    if [ -z "$error" ]; then
      _c="echo -e "o\nn\np\n1\n\n\nw"|fdisk $card_device"
      _o="${_o}\n${_c}\n$($_c 2>&1)"
      [ $? -ne 0 ] && error="$t_sdcard_6"
    fi

    if [ -z "$error" ]; then
      _c="mkfs.vfat -v -n OpenIPC $card_partition"
      _o="${_o}\n${_c}\n$($_c 2>&1)"
      [ $? -ne 0 ] && error="$t_sdcard_7"
    fi

    if [ -z "$error" ]; then
      _c="mount $card_partition $mount_point"
      _o="${_o}\n${_c}\n$($_c 2>&1)"
      [ $? -ne 0 ] && error="$t_sdcard_8"
    fi

    if [ -n "$error" ]; then
      report_error "$error"
      [ -n "$_c" ] && report_command_info "$_c" "$_o"
    else
      report_log "$_o"
    fi
%>
<a class="btn btn-primary" href="/">Go home</a>
<%
  else
    _c="df -h|sed -n 1p/${card_partition////\\\/}/p"
    _o="$($_c)"
    report_command_info "$_c" "$_o"
%>
<div class="alert alert-danger">
  <h4><%= $t_sdcard_9 %></h4>
  <p><%= $t_sdcard_a %></p>
  <form action="<%= $SCRIPT_NAME %>" method="post">
    <% field_hidden "doFormatCard" "true" %>
    <% button_submit "$t_sdcard_b" "danger" %>
  </form>
</div>
<%
  fi
fi
%>
<%in p/footer.cgi %>
