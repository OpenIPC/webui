#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="yadisk"
plugin_name="Yandex Disk"
page_title="Yandex Disk"
config_file="/etc/webui/${plugin}.conf";
tmp_file=/tmp/${plugin}.conf

mkdir -p /etc/webui
[ ! -f "$config_file" ] && touch $config_file

# convert old config format
old_config_file=/etc/yadisk.cfg
if [ -f $old_config_file ]; then
  mv $old_config_file $config_file
  flash_save "success" "Configuration file converted to new format."
fi

if [ "POST" = "$REQUEST_METHOD" ]; then
  :> $config_file
  for v in enabled login password path socks5_enabled; do
    eval echo "${plugin}_${v}=\\\"\$POST_${plugin}_${v}\\\"" >> $config_file
  done
  redirect_to $SCRIPT_NAME
fi

eval $(grep = $config_file)
%>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-xl-3 g-4">
  <div class="col">
    <h3>Yandex Disk</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
<%
field_switch "yadisk_enabled"
field_text "yadisk_login"
field_password "yadisk_password"
field_text "yadisk_path"
field_switch "yadisk_socks5_enabled"
button_submit
%>
    </form>
  </div>
  <div class="col">
    <h3>Config file</h3>
    <% ex "cat $config_file" %>
  </div>
  <div class="col">
    <h3>Preview</h3>
    <p><img src="http://<%= $ipaddr %>/image.jpg" alt="Image: preview" class="img-fluid mb-3" id="preview" width="1280" height="720"></p>
    <% if [ -n "$yadisk_login" ] && [ -n "$yadisk_password" ]; then %>
      <p><a href="#" class="btn btn-primary" id="send-to-yadisk">Send to Yandex Disk</a></p>
    <% fi %>
  </div>
</div>

<%in p/footer.cgi %>
