#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="telegram"
plugin_name="Telegram bot"
page_title="Telegram"

config_file="${ui_config_dir}/${plugin}.conf"
[ ! -f "$config_file" ] && touch $config_file

tmp_file=/tmp/${plugin}.conf

config_file="${ui_config_dir}/${plugin}.conf"
[ ! -f "$config_file" ] && touch $config_file

# convert old config format
old_config_file=/etc/telegram.cfg
if [ -f $old_config_file ]; then
  mv $old_config_file $tmp_file
  if [ -f "$(wc -l $tmp_file | cut -d " " -f 1)" = "2" ]; then
    sed -i "1s/\(.*\)/telegram_token=\"\1\"/" $tmp_file
    sed -i "2s/\(.*\)/telegram_channel=\"\1\"/" $tmp_file
    echo "telegram_enabled=\"true\"" >> $tmp_file
  fi
  mv $tmp_file $config_file
  flash_save "success" "Configuration file converted to new format."
fi
unset old_config_file

if [ "POST" = "$REQUEST_METHOD" ]; then
  :> $tmp_file
  for v in enabled token channel socks5_enabled; do
    eval echo "${plugin}_${v}=\\\"\$POST_${plugin}_${v}\\\"" >> $tmp_file
  done
  unset v
  mv $tmp_file $config_file
  redirect_to $SCRIPT_NAME "success" "Configuration updated."
fi

include $config_file
%>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
  <div class="col">
    <h3>Telegram</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_switch "telegram_enabled" "Enable Telegram bot" %>
      <% field_text "telegram_token" "Token" "Your Telegram Bot authentication token." %>
      <% field_text "telegram_channel" "Chat ID" "Numeric ID of the channel you want the bot to post images to." %>
      <% field_switch "telegram_socks5_enabled" "Use SOCKS5" %>
      <% button_submit %>
    </form>
  </div>
  <div class="col">
    <h3>Config file</h3>
    <% ex "cat $config_file" %>
  </div>
<% if [ -z "$telegram_token" ]; then %>
  <div class="col">
    <h3>How to set up</h3>
    <h4>To create a new channel for your Telegram bot:</h4>
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
  <div class="col">
    <h3>Preview</h3>
    <p><img src="http://<%= $network_address %>/image.jpg" alt="Image: Preview" class="img-fluid mb-3" id="preview" width="1280" height="720"></p>
  <% if [ -n "$telegram_token" ] && [ -n "$telegram_channel" ]; then %>
    <p><a href="#" class="btn btn-primary" id="send-to-telegram">Send to Telegram</a></p>
  <% fi %>
  </div>
</div>

<%in p/footer.cgi %>
