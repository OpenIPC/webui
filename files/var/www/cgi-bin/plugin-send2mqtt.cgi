#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="mqtt"
plugin_name="MQTT client"
page_title="MQTT client"
params="enabled host port client_id username password topic message send_snap snap_topic use_ssl"

[ ! -f /usr/bin/mosquitto_pub ] && redirect_to "/" "danger" "MQTT client is not a part of your firmware."

tmp_file=/tmp/${plugin}.conf

config_file="${ui_config_dir}/${plugin}.conf"
[ ! -f "$config_file" ] && touch $config_file

if [ "POST" = "$REQUEST_METHOD" ]; then
  # parse values from parameters
  for _p in $params; do
    eval ${plugin}_${_p}=\$POST_${plugin}_${_p}
    sanitize "${plugin}_${_p}"
  done; unset _p

  ### Validation
  if [ "true" = "$mqtt_enabled" ]; then
    [ -z "$mqtt_host"      ] && flash_append "danger" "MQTT broker host cannot be empty." && error=11
    [ -z "$mqtt_port"      ] && flash_append "danger" "MQTT port cannot be empty." && error=12
#    [ -z "$mqtt_username"  ] && flash_append "danger" "MQTT username cannot be empty." && error=13
#    [ -z "$mqtt_password"  ] && flash_append "danger" "MQTT password cannot be empty." && error=14
    [ -z "$mqtt_topic"     ] && flash_append "danger" "MQTT topic cannot be empty." && error=15
    [ -z "$mqtt_message"   ] && flash_append "danger" "MQTT message cannot be empty." && error=16
  fi

  if [ "${mqtt_topic:0:1}" = "/" ] || [ "${mqtt_snap_topic:0:1}" = "/" ]; then
    flash_append "danger" "MQTT topic should not start with a slash." && error=17
  fi

  if [ "$mqtt_topic" != "${mqtt_topic// /}" ] || [ "$mqtt_snap_topic" != "${mqtt_snap_topic// /}" ]; then
    flash_append "danger" "MQTT topic should not contain spaces." && error=18
  fi

  if [ -n "$(echo $mqtt_topic | sed -r -n /[^a-zA-Z0-9/]/p)" ] || [ -n "$(echo $mqtt_snap_topic | sed -r -n /[^a-zA-Z0-9/]/p)" ]; then
    flash_append "danger" "MQTT topic should not include non-ASCII characters." && error=19
  fi

  if [ "true" = "$mqtt_send_snap" ] && [ -z "$mqtt_snap_topic" ]; then
    flash_append "danger" "MQTT topic for snapshot should not be empty." && error=20
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

  # Default values
  [ -z "$mqtt_client_id" ] && mqtt_client_id="${network_macaddr//:/}"
  [ -z "$mqtt_port"      ] && mqtt_port="1883"
  [ -z "$mqtt_topic"     ] && mqtt_topic="openipc/${mqtt_client_id}"
  [ -z "$mqtt_message"   ] && mqtt_message=""
fi
%>
<%in p/header.cgi %>

<form action="<%= $SCRIPT_NAME %>" method="post">
<% field_switch "mqtt_enabled" "Enable MQTT client" %>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
      <% field_text "mqtt_host" "MQTT broker host" %>
      <% field_switch "mqtt_use_ssl" "Use SSL" %>
      <% field_text "mqtt_port" "MQTT broker port" %>
      <% field_text "mqtt_client_id" "MQTT client ID" %>
      <% field_text "mqtt_username" "MQTT broker username" %>
      <% field_password "mqtt_password" "MQTT broker password" %>
  </div>
  <div class="col">
      <% field_text "mqtt_topic" "MQTT topic" %>
      <% field_textarea "mqtt_message" "MQTT message" "Supports <a href=\"https://man7.org/linux/man-pages/man3/strftime.3.html \" target=\"_blank\">strftime()</a> format." %>
      <% field_switch "mqtt_send_snap" "Send a snapshot" %>
      <% field_text "mqtt_snap_topic" "MQTT topic to send the snapshot to" %>
      <% field_switch "mqtt_socks5_enabled" "Use SOCKS5" "<a href=\"network-socks5.cgi\">Configure</a> SOCKS5 access" %>
  </div>
  <div class="col">
    <% ex "cat $config_file" %>
    <% button_webui_log %>
  </div>
</div>
  <% button_submit %>
</form>

<script>
$('#mqtt_message').style.height = '7rem';
$('#mqtt_use_ssl').addEventListener('change', evt => {
  const elPort=$('#mqtt_port');
  if (evt.target.checked) {
    if (elPort.value === '1883') elPort.value='8883';
  } else {
    if (elPort.value === '8883') elPort.value='1883';
  }
});
</script>

<%in p/footer.cgi %>
