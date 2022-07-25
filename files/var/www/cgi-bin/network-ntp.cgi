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
      for _i in 0 1 2 3; do
        eval _s="\$POST_ntp_server_${_i}"
        [ -n "$_s" ] && echo "server ${_s} iburst" >> $tmp_file
      done
      unset _i; unset _s
      mv $tmp_file $config_file
      redirect_back "success" "Configuration updated."
      ;;
  esac
fi
%>

<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "update" %>
<%
for _i in 0 1 2 3; do
  _x=$(expr $_i + 1)
  eval ntp_server_${_i}="$(sed -n ${_x}p /etc/ntp.conf | cut -d' ' -f2)"
  field_text "ntp_server_${_i}" "NTP Server $(( _i + 1 ))"
done; unset _i; unset _x
%>
      <% button_submit %>
    </form>
  </div>
  <div class="col">
    <% ex "cat $config_file" %>
    <% if [ "$(diff -q -- "/rom${config_file}" "$config_file")" ]; then %>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "reset" %>
      <% button_submit "Restore firmware defaults" "danger" %>
    </form>
    <% fi %>
  </div>
  <div class="col">
    <p>Camera time: <% date +"%H:%M %Z" %></p>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "sync" %>
      <% button_submit "Synchronize camera time" "primary" %>
    </form>
  </div>
</div>

<%in p/footer.cgi %>
