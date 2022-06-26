#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="socks5"
page_title="SOCKS5 proxy"
config_file="/etc/webui/socks5.conf"

if [ "POST" = "$REQUEST_METHOD" ]; then
  tmp_file=/tmp/${plugin}.conf
  :> $tmp_file
  for v in enabled server port login password; do
    eval echo "${plugin}_${v}=\\\"\$POST_${plugin}_${v}\\\"" >> $tmp_file
  done
  mv $tmp_file $config_file
  redirect_to $SCRIPT_NAME
fi

source $config_file
%>

<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-xxl-3 g-4">
  <div class="col">
    <h3><%= SOCKS5 Proxy Settings %></h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
<%
action="update"
field_hidden "action"
field_text "socks5_server"
field_number "socks5_port"
field_text "socks5_login"
field_password "socks5_password"
button_submit
%>
    </form>
  </div>
  <div class="col">
    <h3>Config file</h3>
    <% ex "cat $config_file" %>
  </div>
</div>

<%in p/footer.cgi %>
