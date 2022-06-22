#!/usr/bin/haserl
<%in _common.cgi %>
<%
plugin="yadisk"
page_title="$t_yadisk_0"
config_file="/etc/${plugin}.cfg"; [ ! -f "$config_file" ] && touch $config_file
url=/cgi-bin/plugin-${plugin}.cgi

if [ "POST" = "$REQUEST_METHOD" ]; then
  :> $config_file
  for v in enabled login password path socks5_enabled socks5_server socks5_port socks5_login socks5_password; do
    eval echo "${plugin}_${v}=\\\"\$POST_${plugin}_${v}\\\"" >> $config_file
  done
  redirect_to "$url"
fi

eval $(grep = $config_file)
%>
<%in _header.cgi %>
<div class="row row-cols-1 row-cols-xl-3 g-3">
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_yadisk_1 %></div>
<div class="card-body">
<form action="<%= $url %>" method="post" autocomplete="off">
<%
field_switch "yadisk_enabled"
field_text "yadisk_login"
field_text "yadisk_password"
field_text "yadisk_path"
field_switch "yadisk_socks5_enabled"
field_text "yadisk_socks5_server"
field_number "yadisk_socks5_port"
field_text "yadisk_socks5_login"
field_text "yadisk_socks5_password"
%>
<button type="submit" class="btn btn-primary mt-3"><%= $t_btn_submit %></button>
</form>
</div>
</div>
</div>

<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_yadisk_2 %></div>
<div class="card-body">
<% ex "cat $config_file" %>
</div>
</div>
</div>

<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_yadisk_3 %></div>
<div class="card-body">
<p><img src="http://<%= $ipaddr %>/image.jpg" alt="Image: preview" class="img-fluid mb-3" id="preview" width="1280" height="720"></p>
<% if [ -n "$yadisk_login" ] && [ -n "$yadisk_password" ]; then %>
<p><a href="#" class="btn btn-primary" id="send-to-yadisk"><%= $t_yadisk_4 %></a></p>
<% fi %>
</div>
</div>
</div>
</div>
<%in p/footer.cgi %>
