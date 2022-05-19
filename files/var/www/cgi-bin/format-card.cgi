#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleFormatCard"
%>
<%in _header.cgi %>
<%
if [ ! -z "$(lsmod | grep mmc)" ]; then
  alert_danger "$tMsgCardNotFound"
else
  card_partition="/dev/mmcblk0p1"
  mount_point="/mnt/mmcblk0p1"
  error=""
  output=""
  if [ -n "$POST_doFormatCard" ]; then
    alert_danger $tMsgCardFormattingTakesTime $tMsgCardFormattingWait
    if [ ! -b $card_partition ]; then
      error="$tMsgNoCardPartition"
    else
      if [ "$(grep $card_partition /etc/mtab)" ]; then
        command="umount $card_partition"
        output="${output}\n$(umount $card_partition 2>&1)"
        [ $? -ne 0 ] && error="$tMsgCannotUnmountCardPartition"
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
<% else %>
<%
command="df -h | grep $card_partition"
output="$(df -h | grep $card_partition 2>&1)"
report_command_info "$command" "$output"
alert_danger "$tMsgCardFormattingDanger" "$tMsgCardFormattingBackup"
%>
<form action="format-card.cgi" method="post">
<input type="hidden" name="doFormatCard" value="true">
<p class="mb-0"><input type="submit" value="<%= $tButtonFormatCard %>" class="btn btn-danger"></p>
</form>
<% fi; fi %>
<%in _footer.cgi %>
