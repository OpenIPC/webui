#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleFormatCard"
%>
<%in _header.cgi %>
<%
ls /dev/mmc* >/dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "<div class=\"alert alert-danger mb-3\">" \
    "<p><b>$tMsgCardNotFoundTitle</b></p>" \
    "<p class=\"mb-0\">$tMsgCardNotFound</p>" \
    "</div>"
else
  card_device="/dev/mmcblk0"
  card_partition="${card_device}p1"
  mount_point="${card_partition//dev/mnt}"
  error=""
  output=""
  if [ -n "$POST_doFormatCard" ]; then
    echo "<div class=\"alert alert-danger mb-3\">" \
      "<p><b>$tMsgCardFormattingTakesTime</b></p>" \
      "<p class=\"mb-0\">$tMsgCardFormattingWait</p>" \
      "</div>"
    if [ ! -b $card_partition ]; then
      error="$tMsgNoCardPartition"
    else
      if [ "$(grep $card_partition /etc/mtab)" ]; then
        command="umount $card_partition"
        output="${output}\n$(umount $card_partition 2>&1)"
        [ $? -ne 0 ] && error="$tMsgCannotUnmountCardPartition"
      fi
      if [ -z "$error" ]; then
        command="echo -e "o\nn\np\n1\n\n\nw" | fdisk /dev/mmcblk0"
        output="${output}\n$(echo -e "o\nn\np\n1\n\n\nw" | fdisk /dev/mmcblk0 2>&1)"
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
    fi
    if [ -n "$error" ]; then
      report_error "$error"
      [ -n "$command" ] && report_command_info "$command" "$output"
    else
%>
<pre class="bg-light p-4 log-scroll">
<% echo -e "$output" %>
</pre>
<% fi %>
<a class="btn btn-primary" href="/"><%= $tButtonGoHome %></a>
<% else
    command="df -h | sed -n 1p/${card_partition////\\\/}/p"
    output="$(df -h | sed -n 1p/${card_partition////\\\/}/p)"
    report_command_info "$command" "$output"
    echo "<div class=\"alert alert-danger mb-3\">" \
      "<p><b>$tMsgCardFormattingDanger</b></p>" \
      "<p>$tMsgCardFormattingBackup</p>" \
      "<form action=\"format-card.cgi\" method=\"post\">" \
      "<input type=\"hidden\" name=\"doFormatCard\" value=\"true\">" \
      "<input type=\"submit\" value=\"$tButtonFormatCard\" class=\"btn btn-danger\">" \
      "</form>" \
      "</div>"
  fi
fi
%>
<%in _footer.cgi %>
