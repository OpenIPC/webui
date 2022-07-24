#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="yadisk"
plugin_name="Yandex Disk"
page_title="Yandex Disk"
params="enabled login password path socks5_enabled"

tmp_file=/tmp/${plugin}.conf
config_file="${ui_config_dir}/${plugin}.conf"
[ ! -f "$config_file" ] && touch $config_file

# convert old config format
old_config_file=/etc/yadisk.cfg
if [ -f $old_config_file ]; then
  mv $old_config_file $config_file
  flash_save "success" "Configuration file converted to new format."
fi

if [ "POST" = "$REQUEST_METHOD" ]; then
  # parse values from parameters
  for _p in $params; do
    eval ${plugin}_${_p}=\$POST_${plugin}_${_p}
    sanitize "${plugin}_${_p}"
  done; unset _p

  ### Validation

  if [ -z "$error" ]; then
    # create temp config file
    :> $tmp_file
    for _p in $params; do
      echo "${plugin}_${_p}=\"$(eval echo \$${plugin}_${_p})\"" >> $tmp_file
    done; unset _p
    mv $tmp_file $config_file

    update_caminfo
    redirect_back "success" "${plugin_name} config updated."
  fi

  redirect_to $SCRIPT_NAME
else
  include $config_file
fi
%>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <h3>Settings</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_switch "yadisk_enabled" "Enable Yandex Disk bot" %>
      <% field_text "yadisk_login" "Yandex Disk login" %>
      <% field_password "yadisk_password" "Yandex Disk password" %>
      <% field_text "yadisk_path" "Yandex Disk path" %>
      <% field_switch "yadisk_socks5_enabled" "Use SOCKS5" "<a href=\"network-socks5.cgi\">Configure</a> SOCKS5 access" %>
      <% button_submit %>
    </form>
  </div>
  <div class="col">
    <h3>Config file</h3>
    <% ex "cat $config_file" %>
  </div>
  <div class="col">
    <h3>Preview</h3>
    <p><img src="http://<%= $network_address %>/image.jpg" alt="Image: preview" class="img-fluid mb-3" id="preview-jpeg" width="1280" height="720"></p>
    <% if [ -n "$yadisk_login" ] && [ -n "$yadisk_password" ]; then %>
      <p><a href="#" class="btn btn-primary" id="send-to-yadisk">Send to Yandex Disk</a></p>
    <% fi %>
  </div>
</div>

<script>
async function updatePreview() {
  await sleep(1000);
  $('#preview-jpeg').src = "http://<%= $network_address %>/image.jpg?t=" + Date.now();
}
$('#preview-jpeg').addEventListener('load', updatePreview);
updatePreview();
</script>

<%in p/footer.cgi %>
