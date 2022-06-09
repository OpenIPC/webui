#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleSdCard"
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
  output=""
  if [ -n "$POST_doFormatCard" ]; then
    alert_ "danger"
    h6 "$tMsgCardFormattingTakesTime"
    p "$tMsgCardFormattingWait"
    _alert

    if [ "$(grep $card_partition /etc/mtab)" ]; then
      command="umount $card_partition"
      output="${output}\n$(umount $card_partition 2>&1)"
      [ $? -ne 0 ] && error="$tMsgCannotUnmountCardPartition"
    fi
    if [ -z "$error" ]; then
      command="echo -e "o\nn\np\n1\n\n\nw" | fdisk $card_device"
      output="${output}\n$(echo -e "o\nn\np\n1\n\n\nw" | fdisk $card_device 2>&1)"
      [ $? -ne 0 ] && error="$tMsgCannotCreatePartition"
    fi
    if [ -z "$error" ]; then
      command="mkfs.vfat -v -n OpenIPC $card_partition"
      output="${output}\n$(mkfs.vfat -v -n OpenIPC $card_partition 2>&1)"
      [ $? -ne 0 ] && error="$tMsgCannotFormatCardPartition"
    fi
    if [ -z "$error" ]; then
      command="mount $card_partition $mount_point"
      output="${output}\n$(mount $card_partition $mount_point 2>&1)"
      [ $? -ne 0 ] && error="$tMsgCannotRemountCardPartition"
    fi
    if [ -n "$error" ]; then
      report_error "$error"
      [ -n "$command" ] && report_command_info "$command" "$output"
    else
      report_log "$output"
    fi
    button_home
  else
    command="df -h | sed -n 1p/${card_partition////\\\/}/p"
    output="$(df -h | sed -n 1p/${card_partition////\\\/}/p)"
    report_command_info "$command" "$output"
    alert_ "danger"
    h6 "$tMsgCardFormattingDanger"
    p "$tMsgCardFormattingBackup"
    form_ "sdcard.cgi" "post"
    doFormatCard="true"
    field_hidden "doFormatCard"
    button_submit "$tButtonFormatCard" "danger"
    _form
    _alert
  fi
fi
%>
<%in _footer.cgi %>
