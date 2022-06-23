#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="bigbro"
page_title="$t_bigbro_0"
config_file="/etc/${plugin}.cfg"; [ ! -f "$config_file" ] && touch $config_file
url=/cgi-bin/plugin-${plugin}.cgi

if [ "POST" = "$REQUEST_METHOD" ]; then
  pin="$POST_bigbro_pin"
  signature=$(echo -ne "$pin"|md5sum|awk '{print $1}')
  sed -d /^${pin}:/ $config_file
  echo "${pin}:${signature}" >> $config_file
  redirect_to "?pin=${pin}"
fi
%>
<%in p/header.cgi %>
<div class="alert alert-warning"><%= $t_alert_1 %></div>
<div class="row row-cols-1 row-cols-xl-3 g-4">
<div class="col">
<h3><%= $t_bigbro_1 %></h3>
<form action="/cgi-bin/plugin-bigbro.cgi" method="post" enctype="multipart/form-data">
<p><%= $t_bigbro_2 %></p>
<div class="mb-2 string">
<label for="bigbro_pin" class="form-label"><%= $t_bigbro_7 %></label>
<input type="text" name="bigbro_pin" id="bigbro_pin" class="form-control" pattern="[A-Za-z0-9]+">
<p class="hint text-secondary"><%= $t_bigbro_8 %></p>
</div>
<button type="submit" class="btn btn-primary mt-3"><%= $t_bigbro_3 %></button>
</form>
</div>
<div class="col">
<h3><%= $t_bigbro_5 %></h3>
<%
if [ -n "$GET_pin" ]; then
  pin="$GET_pin"
  signature=$(grep "^${pin}" $config_file | cut -d: -f2)
%>
<h3><%= $pin %></h3>
<p><%= $signature %></p>
<p><a href="/cgi-bin/plugin-bigbro.cgi" class="btn btn-primary"><%= $t_bigbro_6 %></a></p>
<% else %>
<dl>
<%
for device in $(cat $config_file); do
  pin=${device%:*}
%>
<dt><a href="/cgi-bin/plugin-bigbro.cgi?pin=<%= $pin %>"><%= $pin %></a></dt>
<dd><%= ${device##*:} %></dd>
<% done %>
</dl>
<% fi %>
</div>
<div class="col">
<h3><%= $t_bigbro_4 %></h3>
<% ex "cat $config_file" %>
</div>
</div>
<%in p/footer.cgi %>
