#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="SD Card" %>
<%in p/header.cgi %>
<%
ls /dev/mmc* >/dev/null 2>&1
if [ $? -ne 0 ]; then
%>
<div class="alert alert-danger">
  <h4>Does this camera support SD Card?</h4>
  <p>Your camera does not have an SD Card slot or SD Card is not inserted.</p>
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
  <h4>ATTENTION! SD Card formatting takes time.</h4>
  <p>Please do not refresh this page. Wait until partition formatting is finished!</p>
</div>
<%
    if [ "$(grep $card_partition /etc/mtab)" ]; then
      _c="umount $card_partition"
      _o="${_o}\n${_c}\n$($_c 2>&1)"
      [ $? -ne 0 ] && error="Cannot unmount SD Card partition."
    fi

    if [ -z "$error" ]; then
      _c="echo -e 'o\nn\np\n1\n\n\nw'|fdisk $card_device"
      _o="${_o}\n${_c}\n$($_c 2>&1)"
      [ $? -ne 0 ] && error="Cannot create an SD Card partition."
    fi

    if [ -z "$error" ]; then
      _c="mkfs.vfat -v -n OpenIPC $card_partition"
      _o="${_o}\n${_c}\n$($_c 2>&1)"
      [ $? -ne 0 ] && error="Cannot format SD Card partition."
    fi

    if [ -z "$error" ] && [ ! -d "$mount_point" ]; then
      _c="mkdir -p $mount_point"
      _o="${_o}\n${_c}\n$($_c 2>&1)"
      [ $? -ne 0 ] && error="Cannot create SD Card mount point."
    fi

    if [ -z "$error" ]; then
      _c="mount $card_partition $mount_point"
      _o="${_o}\n${_c}\n$($_c 2>&1)"
      [ $? -ne 0 ] && error="Cannot re-mount SD Card partition."
    fi

    if [ -n "$error" ]; then
      report_error "$error"
      [ -n "$_c" ] && report_command_info "$_c" "$_o"
    else
      report_log "$_o"
    fi
%>
<a class="btn btn-primary" href="/">Go home</a>
<% else %>
<h4># df -h | sed -n "1p/<%= ${card_partition////\\\/} %>/p"</h4>
<pre class="small"><% df -h | sed -n "1p/${card_partition////\\\/}/p" %></pre>

<div class="alert alert-danger">
  <h4>ATTENTION! Formatting will destroy all data on the SD Card.</h4>
  <p>Make sure you have a backup copy if you are going to use the data in the future.</p>
  <form action="<%= $SCRIPT_NAME %>" method="post">
    <% field_hidden "doFormatCard" "true" %>
    <% button_submit "Format SD Card" "danger" %>
  </form>
</div>
<%
  fi
fi
%>
<%in p/footer.cgi %>
