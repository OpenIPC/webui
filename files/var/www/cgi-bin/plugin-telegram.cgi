#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="telegram"
plugin_name="Telegram bot"
page_title="Telegram"
config_file="/etc/webui/${plugin}.cfg"
tmp_file=/tmp/${plugin}.conf

mkdir -p /etc/webui
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

source $config_file
%>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-xxl-3 g-4">
  <div class="col">
    <h3>Telegram</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <p class="boolean">
        <span class="form-check form-switch">
          <input type="hidden" name="telegram_enabled" id="telegram_enabled-false" value="false">
          <input type="checkbox" id="telegram_enabled" name="telegram_enabled" value="true" class="form-check-input" role="switch"<% [ "true" = "$telegram_enabled"] && echo " checked" %>>
          <label for="telegram_enabled" class="form-label form-check-label">Enable Telegram bot</label>
        </span>
      </p>
      <p class="string">
        <label for="telegram_token" class="form-label">Token</label>
        <input type="text" id="telegram_token" name="telegram_token" class="form-control" value="<%= $telegram_token %>">
        <span class="hint text-secondary">Your Telegram Bot authentication token.</span>
      </p>
      <p class="string">
        <label for="telegram_channel" class="form-label">Chat ID</label>
        <input type="text" id="telegram_channel" name="telegram_channel" class="form-control" value="<%= $telegram_channel %>">
        <span class="hint text-secondary">Numeric ID of the channel you want the bot to post images to.</span>
      </p>
      <p class="boolean">
        <span class="form-check form-switch">
        <input type="hidden" name="telegram_socks5_enabled" id="telegram_socks5_enabled-false" value="false">
        <input type="checkbox" id="telegram_socks5_enabled" name="telegram_socks5_enabled" value="true" class="form-check-input" role="switch"<% [ "true" = "$telegram_socks5_enabled"] && echo " checked" %>>
        <label for="telegram_socks5_enabled" class="form-label form-check-label">Use SOCKS5</label>
      </span>
      </p>
      <p class="mt-2"><input type="submit" class="btn btn-primary" value="Save changes"></p>
    </form>
  </div>
  <div class="col">
    <h3>Config file</h3>
    <% ex "cat $config_file" %>
  </div>
<% if [ ! -z "$telegram_token" ]; then %>
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
    <p><img src="http://<%= $ipaddr %>/image.jpg" alt="Image: Preview" class="img-fluid mb-3" id="preview" width="1280" height="720"></p>
  <% if [ -n "$telegram_token" ] && [ -n "$telegram_channel" ]; then %>
    <p><a href="#" class="btn btn-primary" id="send-to-telegram">Send to Telegram</a></p>
  <% fi %>
  </div>
</div>

<%in p/footer.cgi %>
