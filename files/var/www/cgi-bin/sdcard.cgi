#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPT_SdCard"
%>
<%in _header.cgi %>
<%
ls /dev/mmc* >/dev/null 2>&1
if [ $? -ne 0 ]; then
  alert_ "danger"
  h6 "$tMsgCardNotFoundTitle"
  p "$tMsgCardNotFound"
  _alert
else
  card_device="/dev/mmcblk0"
  card_partition="${card_device}p1"
  mount_point="${card_partition//dev/mnt}"
  error=""
  _o=""
  if [ -n "$POST_doFormatCard" ]; then
    alert_ "danger"
    h6 "$tMsgCardFormattingTakesTime"
    p "$tMsgCardFormattingWait"
    _alert
    if [ "$(grep $card_partition /etc/mtab)" ]; then
      _c="umount $card_partition"
      _o="${_o}\n${_c}\n$($_c 2>&1)"
      [ $? -ne 0 ] && error="$tMsgCannotUnmountCardPartition"
    fi
    if [ -z "$error" ]; then
      _c="echo -e "o\nn\np\n1\n\n\nw"|fdisk $card_device"
      _o="${_o}\n${_c}\n$($_c 2>&1)"
      [ $? -ne 0 ] && error="$tMsgCannotCreatePartition"
    fi
    if [ -z "$error" ]; then
      _c="mkfs.vfat -v -n OpenIPC $card_partition"
      _o="${_o}\n${_c}\n$($_c 2>&1)"
      [ $? -ne 0 ] && error="$tMsgCannotFormatCardPartition"
    fi
    if [ -z "$error" ]; then
      _c="mount $card_partition $mount_point"
      _o="${_o}\n${_c}\n$($_c 2>&1)"
      [ $? -ne 0 ] && error="$tMsgCannotRemountCardPartition"
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
    h6 "$tMsgCardFormattingDanger"
    p "$tMsgCardFormattingBackup"
    form_ "sdcard.cgi"
    doFormatCard="true"
    field_hidden "doFormatCard"
    button_submit "$tB_FormatCard" "danger"
    _form
    _alert
  fi
fi
%>
<%in p/footer.cgi %>
