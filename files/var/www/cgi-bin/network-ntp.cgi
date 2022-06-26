#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="ntp"
page_title="NTP servers"
config_file="/etc/ntp.conf"

if [ "POST" = "$REQUEST_METHOD" ]; then
  case "$POST_action" in
    reset)
      cp /rom/etc/ntp.conf /etc/ntp.conf
      redirect_to $SCRIPT_NAME "success" "Configuration reset to firware defaults."
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
      redirect_to $SCRIPT_NAME "success" "Configuration updated."
      ;;
  esac
fi
%>

<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-xxl-3 g-4">
  <div class="col">
    <h3>NTP Servers</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <input type="hidden" name="action" value="update">
<%
for i in 0 1 2 3; do
  x=$(expr $i + 1)
  eval "ntp_server_${i}=$(sed -n ${x}p /etc/ntp.conf | cut -d' ' -f2)"
  field_text "ntp_server_${i}"
done
%>
      <p class="mt-2"><input type="submit" class="btn btn-danger" value="Save changes"></p>
    </form>
  </div>
  <div class="col">
    <h3>NTP Settings</h3>
    <% ex "cat $config_file" %>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <input type="hidden" name="action" value="reset">
      <p class="mt-2"><input type="submit" class="btn btn-danger" value="Reset to firware defaults"></p>
    </form>
  </div>
</div>

<%in p/footer.cgi %>
