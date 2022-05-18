#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleFormatCard"
%>
<%in _header.cgi %>
<div class="alert alert-danger">
<b>ATTENTION! SD card formatting takes time.</b>
<p class="mb-0">Please do not refresh this page, wait until partition formatting is finished.</p>
</div>
<%
card_partition="/dev/mmcblk0p1"
mount_point="/mnt/mmcblk0p1"
error=""
output=""
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
<%in _footer.cgi %>
