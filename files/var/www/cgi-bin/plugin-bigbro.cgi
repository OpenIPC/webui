#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="bigbro"
plugin_name="BigBro"
page_title="BigBro"
config_file="${config_path}/${plugin}.cfg"
[ ! -f "$config_file" ] && touch $config_file

# source $config_file

case "$REQUEST_METHOD" in
  POST)
    pin="$POST_bigbro_pin"
    signature=$(echo -ne "$pin"|md5sum|awk '{print $1}')
    sed -d /^${pin}:/ $config_file
    echo "${pin}:${signature}" >> $config_file
    redirect_to "${SCRIPT_NAME}?pin=${pin}"
    ;;
  GET)
%>
<%in p/header.cgi %>
<div class="alert alert-warning"><%= $t_alert_1 %></div>
<div class="row row-cols-1 row-cols-xl-3 g-4">
  <div class="col">
    <h3>Add a device</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post" enctype="multipart/form-data">
      <p>Please enter access PIN to add a device.</p>
      <p class="string">
        <label for="bigbro_pin" class="form-label">Access PIN</label>
        <input type="text" name="bigbro_pin" id="bigbro_pin" class="form-control" pattern="[A-Za-z0-9]+" title="letters and numbers, no punctuation or special characters" required>
      </p>
      <p class="submit">
        <input type="submit" class="btn btn-primary mt-3" value="Add device">
      </p>
    </form>
  </div>
  <div class="col">
    <h3>Devices</h3>
    <% if [ -n "$GET_pin" ]; then %>
      <h4><%= $GET_pin %></h4>
      <p><% grep ^${GET_pin}: $config_file | cut -d: -f2 %></p>
      <p><a href="<%= $SCRIPT_NAME %>" class="btn btn-primary">List of devices</a></p>
    <% else %>
      <dl>
      <% for device in $(cat $config_file); do pin=${device%:*} %>
        <dt><a href="<%= $SCRIPT_NAME %>?pin=<%= $pin %>"><%= $pin %></a></dt>
        <dd><%= ${device##*:} %></dd>
      <% done %>
      </dl>
    <% fi %>
  </div>
  <div class="col">
    <h3>Config file</h3>
    <% ex "cat $config_file" %>
  </div>
</div>
<%in p/footer.cgi %>
<%
;;
esac
%>
