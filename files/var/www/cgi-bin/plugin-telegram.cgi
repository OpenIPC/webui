#!/usr/bin/haserl
<%in _common.cgi %>
<%
plugin="telegram"
page_title="$tPageTitlePluginTelegram"
config_file="/etc/${plugin}.cfg"; [ ! -f "$config_file" ] && touch $config_file
url=/cgi-bin/plugin-${plugin}.cgi

if [ -n "$POST_action" ] && [ "$POST_action" = "reset" ]; then
  mv $config_file ${config_file}.backup
  redirect_to $url
fi

if [ -n "$POST_token" ]; then
  echo "$POST_token" > $config_file
  echo "$POST_channel" >> $config_file
  redirect_to $url
fi

telegram_token=$(sed -n 1p $config_file)
telegram_channel=$(sed -n 2p $config_file)
%>
<%in _header.cgi %>
<%
row_ "row-cols-1 row-cols-xl-2 g-3 mb-3"
  col_card_ "$tHeaderTelegramBot"
    form_ $url "post"
      extras=""; [ -n "$telegram_token" ] && extras="${extras} disabled"
      field_text "telegram_token" "$extras"
      extras=""; [ -n "$telegram_channel" ] && extras="${extras} disabled"
      field_text "telegram_channel" "$extras"
      if [ $(cat $config_file | wc -l) -ge 2 ]; then
        button_submit_action "reset" "$tButtonResetConfig" "data-method=\"delete\""
      else
        button_submit "$tButtonFormSubmit" "primary"
      fi
    _form
  _col_card

  if [ -z "$token" ]; then
    col_first
      alert_ "info"
      h6 "$tMsgTelegramCreateChannelHeader"
      ol_
        li "$tMsgTelegramCreateChannelStep1"
        li "$tMsgTelegramCreateChannelStep2"
        li "$tMsgTelegramCreateChannelStep3"
        li "$tMsgTelegramCreateChannelStep4"
        li "$tMsgTelegramCreateChannelStep5"
        li "$tMsgTelegramCreateChannelStep6"
      _ol
    _alert
    col_last
  fi
_row
%>
<%in _footer.cgi %>
