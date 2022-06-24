#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="$t_sdcard_0" %>
<%in p/header.cgi %>
<%
ls /dev/mmc* >/dev/null 2>&1
if [ $? -ne 0 ]; then
  alert_ "danger"
    h4 "$t_sdcard_1"
    p "$t_sdcard_2"
  _alert
else
  card_device="/dev/mmcblk0"
  card_partition="${card_device}p1"
  mount_point="${card_partition//dev/mnt}"
  error=""
  _o=""
  if [ -n "$POST_doFormatCard" ]; then
    alert_ "danger"
      h4 "$t_sdcard_3"
      p "$t_sdcard_4"
    _alert

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

    button_home
  else
    _c="df -h|sed -n 1p/${card_partition////\\\/}/p"
    _o="$($_c)"
    report_command_info "$_c" "$_o"
    alert_ "danger"
      h4 "$t_sdcard_9"
      p "$t_sdcard_a"
      form_ "sdcard.cgi"
        doFormatCard="true"
        field_hidden "doFormatCard"
        button_submit "$t_sdcard_b" "danger"
      _form
    _alert
  fi
fi
%>
<%in p/footer.cgi %>
