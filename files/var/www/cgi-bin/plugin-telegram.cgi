#!/usr/bin/haserl
<%in _common.cgi %>
<%
plugin="telegram"
page_title="$t_telegram_0"
config_file="/etc/${plugin}.cfg"; [ ! -f "$config_file" ] && touch $config_file
url=/cgi-bin/plugin-${plugin}.cgi

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
  redirect_to "$url"
fi

eval $(grep = $config_file)
%>
<%in _header.cgi %>

<div class="row row-cols-1 row-cols-xxl-3 g-3">
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_telegram_2 %></div>
<div class="card-body">
<form action="<%= $url %>" method="post" autocomplete="off">
<%
field_switch "telegram_enabled"
field_text "telegram_token"
field_text "telegram_channel"
field_switch "telegram_socks5_enabled"
field_text "telegram_socks5_server"
field_number "telegram_socks5_port"
field_text "telegram_socks5_login"
field_text "telegram_socks5_password"
%>
<button type="submit" class="btn btn-primary mt-3"><%= $t_btn_submit %></button>
</form>
</div>
</div>
</div>
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_telegram_3 %></div>
<div class="card-body">
<% ex "cat $config_file" %>
</div>
</div>
</div>

<% if [ ! -z "$telegram_token" ]; then %>
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_telegram_4 %></div>
<div class="card-body">
<h6><%= $t_telegram_5 %></h6>
<ol>
<li><%= $t_telegram_6 %></li>
<li><%= $t_telegram_7 %></li>
<li><%= $t_telegram_8 %></li>
<li><%= $t_telegram_9 %></li>
<li><%= $t_telegram_a %></li>
<li><%= $t_telegram_b %></li>
</ol>
</div>
</div>
</div>
<% fi %>

<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_telegram_c %></div>
<div class="card-body">
<p><img src="http://<%= $ipaddr %>/image.jpg" alt="Image: Preview" class="img-fluid mb-3" id="preview" width="1280" height="720"></p>
<% if [ -n "$telegram_token" ] && [ -n "$telegram_channel" ]; then %>
<p><a href="#" class="btn btn-primary" id="send-to-telegram"><%= $t_telegram_d %></a></p>
<% fi %>
</div>
</div>
</div>
</div>
<%in p/footer.cgi %>
