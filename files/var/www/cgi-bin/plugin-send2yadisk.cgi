#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="yadisk"
plugin_name="Send to Yandex Disk"
page_title="Send to Yandex Disk"
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
unset old_config_file

if [ "POST" = "$REQUEST_METHOD" ]; then
  # parse values from parameters
  for _p in $params; do
    eval ${plugin}_${_p}=\$POST_${plugin}_${_p}
    sanitize "${plugin}_${_p}"
  done; unset _p

  ### Validation
  if [ "true" = "$email_enabled" ]; then
    [ -z "$yadisk_login"    ] && flash_append "danger" "Yandex Disk login cannot be empty." && error=11
    [ -z "$yadisk_password" ] && flash_append "danger" "Yandex Disk password cannot be empty." && error=12
  fi

  if [ -z "$error" ]; then
    # create temp config file
    :>$tmp_file
    for _p in $params; do
      echo "${plugin}_${_p}=\"$(eval echo \$${plugin}_${_p})\"" >>$tmp_file
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

<form action="<%= $SCRIPT_NAME %>" method="post">
  <% field_switch "yadisk_enabled" "Enable Yandex Disk bot" %>
  <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
    <div class="col">
      <% field_text "yadisk_login" "Yandex Disk login" %>
      <% field_password "yadisk_password" "Yandex Disk password" "Create a dedicated password for application (WebDAV)." %>
      <% field_text "yadisk_path" "Yandex Disk path" %>
      <% field_switch "yadisk_socks5_enabled" "Use SOCKS5" "<a href=\"network-socks5.cgi\">Configure</a> SOCKS5 access" %>
      <% button_submit %>
    </div>
  </form>
  <div class="col">
    <% ex "cat $config_file" %>
  </div>
  <div class="col">
    <% preview %>
    <% if [ "true" = "$yadisk_enabled" ]; then %>
      <p><a href="#" class="btn btn-primary" id="send-to-yadisk">Send to Yandex Disk</a></p>
    <% fi %>
  </div>
</div>

<% [ -f "/tmp/webui/${plugin}.log" ] && ex "cat /tmp/webui/${plugin}.log" %>

<%in p/footer.cgi %>
