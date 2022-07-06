#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="bigbro"
plugin_name="BigBro"
page_title="BigBro"

config_file="${ui_config_dir}/${plugin}.conf"
[ ! -f "$config_file" ] && touch $config_file

# include $config_file

case "$REQUEST_METHOD" in
  POST)
    pin="$POST_bigbro_pin"
    signature=$(echo -ne "$(date +%s):$pin"|md5sum|awk '{print $1}')
    sed -i /^${pin}:/d $config_file
    echo "${pin}:${signature}" >> $config_file
    redirect_to "${SCRIPT_NAME}?pin=${pin}"
    ;;
  GET)
%>
<%in p/header.cgi %>

<p class="alert alert-warning">Attention! This is only a proof of concept for the prospective subsystem of additional services. No real functionality here.</p>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <h3>Add a device</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post" enctype="multipart/form-data">
      <p>Please enter access PIN to add a device.</p>
      <% field_text "bigbro_pin" "Access PIN" %>
      <% button_submit "Add device" %>
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

<script>
const el=$("#bigbro_pin")
el.pattern = "[A-Za-z0-9]+";
el.title = "letters and numbers, no punctuation or special characters"
el.required = true;
</script>

<%in p/footer.cgi %>
<%
;;
esac
%>
