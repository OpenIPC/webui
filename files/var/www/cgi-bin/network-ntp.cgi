#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="ntp"
page_title="Time Synchronization"

config_file="/etc/${plugin}.conf"
[ ! -f "$config_file" ] && touch $config_file

if [ "POST" = "$REQUEST_METHOD" ]; then
  case "$POST_action" in
    reset)
      cp /rom/etc/ntp.conf /etc/ntp.conf
      redirect_back "success" "Configuration reset to firware defaults."
      ;;
    sync)
      /usr/sbin/ntpd -n -q -N
      if [ $? -eq 0 ]; then
        redirect_back "success" "Camera time synchronized with NTP server."
      else
        redirect_back "danger" "Synchronization failed!"
      fi
      ;;
    update)
      tmp_file=/tmp/${plugin}.conf
      :> $tmp_file
      for i in 0 1 2 3; do
        eval s=\$POST_ntp_server_${i}
        [ -n "$s" ] && echo "server ${s} iburst" >> $tmp_file
      done
      unset i; unset s
      mv $tmp_file $config_file
      redirect_back "success" "Configuration updated."
      ;;
  esac
fi
%>

<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-xxl-3 g-4">
  <div class="col">
    <h3>NTP Servers</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
<%
field_hidden "action" "update"
for i in 0 1 2 3; do
  x=$(expr $i + 1)
  eval "ntp_server_${i}=$(sed -n ${x}p /etc/ntp.conf | cut -d' ' -f2)"
  field_text "ntp_server_${i}" "NTP Server $(( i + 1 ))"
done
button_submit
%>
    </form>
  </div>
  <div class="col">
    <h3>NTP Settings</h3>
    <% ex "cat $config_file" %>
    <% if [ "$(diff -q -- "/rom${config_file}" "$config_file")" ]; then %>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "reset" %>
      <% button_submit "Restore firmware defaults" "danger" %>
    </form>
    <% fi %>
  </div>
  <div class="col">
    <h3>Camera time</h3>
    <h4 class="display-1 text-center bg-light"><% date +%H:%M %></h4>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "sync" %>
      <% button_submit "Synchronize camera time" "primary" %>
    </form>
  </div>
</div>

<%in p/footer.cgi %>
