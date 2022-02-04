#!/usr/bin/haserl
<%in _common.cgi %>
<%
plugin="telegram"
page_title="$tPageTitlePluginTelegram"
config_file="/etc/${plugin}.cfg"
[ ! -f "$config_file" ] && touch ${config_file}

if [ -n "$POST_action" ] && [ "$POST_action" = "reset" ]; then
  mv ${config_file} ${config_file}.backup
  redirect_to "/cgi-bin/plugin-telegram.cgi"
fi

if [ -n "$POST_token" ]; then
  token="$POST_token"
  channel="$POST_channel"
  echo "${token}" > ${config_file}
  echo "${channel}" >> ${config_file}
  redirect_to "/cgi-bin/plugin-telegram.cgi"
fi

token=$(sed -n 1p ${config_file})
channel=$(sed -n 2p ${config_file})
%>
<%in _header.cgi %>
<div class="row">
  <div class="col-md-6 mb-3">
    <div class="card">
      <div class="card-header"><%= $tHeaderTelegramBot %></div>
      <div class="card-body">
        <form action="/cgi-bin/plugin-telegram.cgi" method="post">
          <div class="row mb-3">
            <div class="col-2">
              <label class="form-label" for="username"><%= $tLabelTelegramToken %></label>
            </div>
            <div class="col-auto">
              <input class="form-control" type="text" id="token" name="token" value="<%= $token %>" size="45"<% [ -n "$token" ] && echo -n " disabled" %>>
            </div>
            <div class="col-auto">
              <span id="tokenHelpBlock" class="form-text"><%= $tHintTelegramToken %></span>
            </div>
          </div>
          <div class="row mb-3">
            <div class="col-lg-2">
              <label class="form-label" for="channel"><%= $tLabelTelegramChatId %></label>
            </div>
            <div class="col-auto">
              <input class="form-control" type="text" id="channel" name="channel" value="<%= $channel %>" size="15"<% [ -n "$channel" ] && echo -n " disabled" %>>
            </div>
            <div class="col-auto">
              <span id="channelHelpBlock" class="form-text"><%= $tHintTelegramChatId %></span>
            </div>
          </div>
          <% if [ $(cat /etc/telegram.cfg | wc -l) -ge 2 ]; then %>
            <button type="submit" class="btn btn-danger" data-method="delete" name="action" value="reset"><%= $tButtonResetConfig %></button>
          <% else %>
            <button type="submit" class="btn btn-primary"><%= $tButtonFormSubmit %></button>
          <% fi %>
        </form>
      </div>
    </div>
  </div>
<% if [ -z "$token" ]; then %>
  <div class="col mb-3">
    <h5><%= $tMsgTelegramCreateChannelHeader %></h5>
    <ol>
      <li><%= $tMsgTelegramCreateChannelStep1 %> <a href="https://t.me/BotFather">BotFather</a>.</li>
      <li><%= $tMsgTelegramCreateChannelStep2 %></li>
      <li><%= $tMsgTelegramCreateChannelStep3 %></li>
      <li><%= $tMsgTelegramCreateChannelStep4 %></li>
      <li><%= $tMsgTelegramCreateChannelStep5 %></li>
      <li><%= $tMsgTelegramCreateChannelStep6 %></li>
    </ol>
  </div>
<% fi %>
</div>
<%in _footer.cgi %>
