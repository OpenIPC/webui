#!/usr/bin/haserl
<%in _common.cgi %>
<%
plugin="yadisk"
page_title="$tPageTitlePluginYandexDisk"
config_file="/etc/${plugin}.cfg"; [ ! -f "$config_file" ] && touch $config_file
url=/cgi-bin/plugin-${plugin}.cgi

if [ "POST" = "$REQUEST_METHOD" ]; then
  :> $config_file
  for v in enabled login password path socks5_enabled socks5_server socks5_port socks5_login socks5_password; do
    eval echo "${plugin}_${v}=\\\"\$POST_${plugin}_${v}\\\"" >> $config_file
  done
  redirect_to $url
fi

eval $(grep = $config_file)
%>
<%in _header.cgi %>
<%
form_ $url "post"
  row_ "row-cols-1 row-cols-xl-3 g-3"
    col_card_ "$tHeaderYandexDiskSettings"
      field_switch "yadisk_enabled"
      field_text "yadisk_login"
      field_text "yadisk_password"
      field_text "yadisk_path"
      field_switch "yadisk_socks5_enabled"
      field_text "yadisk_socks5_server"
      field_number "yadisk_socks5_port"
      field_text "yadisk_socks5_login"
      field_text "yadisk_socks5_password"
    _col_card
    col_card_ "$tHeaderYandexDiskPluginConfig"
      pre_
        echo "$(cat $config_file)"
      _pre
    _col_card
    col_card_ "Preview"
      image "http://${ipaddr}/image.jpg" "id=\"preview\" class=\"img-fluid mb-3\" width=\"1280\" height=\"720\""
      if [ -n "$yadisk_login" ] && [ -n "$yadisk_password" ]; then
        link_to "Send to Yandex Disk" "#" "class=\"btn btn-primary \" id=\"send-to-yadisk\""
      fi
    _col_card
  _row

  button_submit "$tButtonFormSubmit" "primary"
_form
%>
<%in _footer.cgi %>
