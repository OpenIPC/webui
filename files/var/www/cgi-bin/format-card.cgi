#!/usr/bin/haserl
<%in _common.cgi %>
<%in _header.cgi %>
<%
page_title=$tPageTitleFormatCard
card_partition="/dev/mmcblk0p1"
if [ ! -b $card_partition ]; then
  report_error "$tMsgNoCardPartition"
else
%>
<pre class="bg-light p-4 log-scroll">
<%
umount $card_partition && mkfs.vfat -n OpenIPC $card_partition || echo "Cannot unmount $card_partition"
%>
</pre>
<% fi %>
<a class="btn btn-primary" href="/"><%= $tButtonGoHome %></a>
<%in _footer.cgi %>
