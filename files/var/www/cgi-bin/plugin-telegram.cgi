#!/usr/bin/haserl
<%in _common.cgi %>
<%
plugin="telegram"
page_title="Telegram Bot"
config_file="/etc/${plugin}.cfg"
[ ! -f "$config_file" ] && touch ${config_file}

if [ -n "$POST_token" ]; then
  token="$POST_token"
  channel="$POST_channel"
  echo "${token}" > ${config_file}
  echo "${channel}" >> ${config_file}
  redirect_to "/cgi-bin/plugin-telegram.cgi"
else
  token=$(sed -n 1p ${config_file})
  channel=$(sed -n 2p ${config_file})
fi
%>
<%in _header.cgi %>
<div class="row">
  <div class="col-md-6 mb-3">
    <div class="card">
      <div class="card-header">Telegram Bot</div>
      <div class="card-body">
        <form action="/cgi-bin/plugin-telegram.cgi" method="post">
          <div class="row mb-3">
            <div class="col-2">
              <label class="form-label" for="username">Token</label>
            </div>
            <div class="col-auto">
              <input class="form-control" type="text" id="token" name="token" value="<%= $token %>" size="45"<% [ -n "$token" ] && echo -n " disabled" %>>
            </div>
            <div class="col-auto">
              <span id="tokenHelpBlock" class="form-text">Your Telegram Bot authentication token.</span>
            </div>
          </div>
          <div class="row mb-3">
            <div class="col-lg-2">
              <label class="form-label" for="channel">Chat ID</label>
            </div>
            <div class="col-auto">
              <input class="form-control" type="text" id="channel" name="channel" value="<%= $channel %>" size="15"<% [ -n "$channel" ] && echo -n " disabled" %>>
            </div>
            <div class="col-auto">
              <span id="channelHelpBlock" class="form-text">Numeric ID of the channel you want the bot to post images to.</span>
            </div>
          </div>
          <% if [ $(cat /etc/telegram.cfg | wc -l) -eq 2 ]; then %>
            <button type="button" class="btn btn-danger" data-method="delete">Reset configuration</button>
          <% else %>
            <button type="submit" class="btn btn-primary">Save configuration</button>
          <% fi %>
        </form>
      </div>
    </div>
  </div>
<% if [ -z "$token" ]; then %>
  <div class="col mb-3">
    <h5>To create a new channel for your Telegram bot:</h5>
    <ol>
      <li>Start a chat with <a href="https://t.me/BotFather">BotFather</a>.</li>
      <li>Enter <code>/start</code> to start a session.</li>
      <li>Enter <code>/newbot</code> to create a new bot.</li>
      <li>Give your bot channel a name, e.g. <i>cool_cam_bot</i>.</li>
      <li>Give your bot a username, e.g. <i>CoolCamBot</i>.</li>
      <li>Copy the token assigned to your new bot by the BotFather, and paste it to the form.</li>
    </ol>
  </div>
<% fi %>
</div>
<%in _footer.cgi %>
