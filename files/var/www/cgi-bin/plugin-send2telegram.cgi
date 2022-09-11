#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="telegram"
plugin_name="Send to Telegram"
page_title="Send to Telegram"
params="enabled token channel socks5_enabled"

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
  if [ "true" = "$telegram_enabled" ]; then
    [ -z "$telegram_token"   ] && flash_append "danger" "Telegram token cannot be empty." && error=11
    [ -z "$telegram_channel" ] && flash_append "danger" "Telegram channel cannot be empty." && error=12
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

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_switch "telegram_enabled" "Enable sending to Telegram" %>
      <% field_text "telegram_token" "Token" "Your Telegram Bot authentication token." %>
      <% field_text "telegram_channel" "Chat ID" "Numeric ID of the channel you want the bot to post images to." %>
      <% field_switch "telegram_socks5_enabled" "Use SOCKS5" "<a href=\"network-socks5.cgi\">Configure</a> SOCKS5 access" %>
      <% button_submit %>
    </form>
  </div>
  <div class="col">
    <% ex "cat $config_file" %>
    <% [ -f "/tmp/webui.log" ] && link_to "Download log file" "dl.cgi" %>
  </div>
</div>

<% if [ -z "$telegram_token" ]; then %>
<div class="alert alert-info mt-4">
  <h5>To create a channel for your Telegram bot:</h5>
  <ol>
    <li>Start a chat with <a href=\"https://t.me/BotFather\">@BotFather</a></li>
    <li>Enter <code>/start</code> to start a session.</li>
    <li>Enter <code>/newbot</code> to create a new bot.</li>
    <li>Give your bot channel a name, e.g. <i>cool_cam_bot</i>.</li>
    <li>Give your bot a username, e.g. <i>CoolCamBot</i>.</li>
    <li>Copy the token assigned to your new bot by the BotFather, and paste it to the form.</li>
  </ol>
</div>
<% fi %>

<%in p/footer.cgi %>
