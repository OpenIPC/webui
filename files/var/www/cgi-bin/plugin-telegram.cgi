#!/usr/bin/haserl
<%in _common.cgi %>
<%
plugin="telegram"
page_title="$tPageTitlePluginTelegram"
config_file="/etc/${plugin}.cfg"; [ ! -f "$config_file" ] && touch $config_file
url=/cgi-bin/plugin-${plugin}.cgi

# convert old config format
if [ "$(wc -l $config_file | cut -d " " -f 1)" = "2" ]; then
  sed -i "1s/\(.*\)/telegram_token=\"\1\"/" $config_file
  sed -i "2s/\(.*\)/telegram_channel=\"\1\"/" $config_file
  echo "telegram_enabled=\"true\"" >> $config_file
  flash_save "success" "Configuration file converted to new format."
fi

if [ "POST" = "$REQUEST_METHOD" ]; then
  :> $config_file
  for v in enabled token channel; do
    eval echo "${plugin}_${v}=\\\"\$POST_${plugin}_${v}\\\"" >> $config_file
  done
  redirect_to $url
fi

eval $(grep = $config_file)
%>
<%in _header.cgi %>
<%
row_ "row-cols-1 row-cols-xxl-3 g-3"
  col_card_ "$tHeaderTelegramBot"
    form_ $url "post"
      field_switch "telegram_enabled"
      field_text "telegram_token"
      field_text "telegram_channel"
      button_submit "$tButtonFormSubmit" "primary"
    _form
  _col_card
  col_card_ "$tHeaderTelegramPluginConfig"
    pre_
      echo "$(cat $config_file)"
    _pre
  _col_card
  if [ -z "$telegram_token" ]; then
    col_card_ "How to set up"
      h6 "$tMsgTelegramCreateChannelHeader"
      ol_
        li "$tMsgTelegramCreateChannelStep1"
        li "$tMsgTelegramCreateChannelStep2"
        li "$tMsgTelegramCreateChannelStep3"
        li "$tMsgTelegramCreateChannelStep4"
        li "$tMsgTelegramCreateChannelStep5"
        li "$tMsgTelegramCreateChannelStep6"
      _ol
    _col_card
  else
    col_card_ "Preview"
      image "http://${ipaddr}/image.jpg" "id=\"preview\" class=\"img-fluid mb-3\" width=\"1280\" height=\"720\""
      if [ -n "$telegram_token" ] && [ -n "$telegram_channel" ]; then
        link_to "Send to Telegram" "#" "class=\"btn btn-primary \" id=\"send-to-telegram\""
      fi
    _col_card
  fi
_row
%>
<%in _footer.cgi %>
