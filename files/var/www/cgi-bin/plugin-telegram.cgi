#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="telegram"
plugin_name="Telegram"
page_title="$t_telegram_0"
config_file="/etc/${plugin}.cfg"; [ ! -f "$config_file" ] && touch $config_file

# convert old config format
if [ "$(wc -l $config_file | cut -d " " -f 1)" = "2" ]; then
  sed -i "1s/\(.*\)/telegram_token=\"\1\"/" $config_file
  sed -i "2s/\(.*\)/telegram_channel=\"\1\"/" $config_file
  echo "telegram_enabled=\"true\"" >> $config_file
  flash_save "success" "$t_telegram_1"
fi

if [ "POST" = "$REQUEST_METHOD" ]; then
  :> $config_file
  for v in enabled token channel socks5_enabled socks5_server socks5_port socks5_login socks5_password; do
  eval echo "${plugin}_${v}=\\\"\$POST_${plugin}_${v}\\\"" >> $config_file
  done
  redirect_to $SCRIPT_NAME
fi

eval $(grep = $config_file)
%>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-xxl-3 g-4">
  <div class="col">
    <h3><%= $t_telegram_2 %></h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
<%
field_switch "telegram_enabled"
field_text "telegram_token"
field_text "telegram_channel"
field_switch "telegram_socks5_enabled"
field_text "telegram_socks5_server"
field_number "telegram_socks5_port"
field_text "telegram_socks5_login"
field_text "telegram_socks5_password"
button_submit
%>
    </form>
  </div>
  <div class="col">
    <h3><%= $t_telegram_3 %></h3>
    <% ex "cat $config_file" %>
  </div>
<% if [ ! -z "$telegram_token" ]; then %>
  <div class="col">
    <h3><%= $t_telegram_4 %></h3>
    <h4><%= $t_telegram_5 %></h4>
    <ol>
      <li><%= $t_telegram_6 %></li>
      <li><%= $t_telegram_7 %></li>
      <li><%= $t_telegram_8 %></li>
      <li><%= $t_telegram_9 %></li>
      <li><%= $t_telegram_a %></li>
      <li><%= $t_telegram_b %></li>
    </ol>
  </div>
<% fi %>
  <div class="col">
    <h3><%= $t_telegram_c %></h3>
    <p><img src="http://<%= $ipaddr %>/image.jpg" alt="Image: Preview" class="img-fluid mb-3" id="preview" width="1280" height="720"></p>
  <% if [ -n "$telegram_token" ] && [ -n "$telegram_channel" ]; then %>
    <p><a href="#" class="btn btn-primary" id="send-to-telegram"><%= $t_telegram_d %></a></p>
  <% fi %>
  </div>
</div>

<%in p/footer.cgi %>
