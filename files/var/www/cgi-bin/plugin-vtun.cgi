#!/usr/bin/haserl
<%in _common.cgi %>
<%
plugin="vtun"
url=/cgi-bin/plugin-vtun.cgi
page_title="$t_vtun_0"
service_file=/etc/init.d/S98vtun

if [ -n "$POST_action" ] && [ "$POST_action" = "reset" ]; then
  killall tunnel
  killall vtund
  rm $service_file
  redirect_to "$url"
fi

if [ -n "$POST_vtun_server" ]; then
  echo -e "#!/bin/sh\n\ntunnel $POST_vtun_server" > $service_file
  chmod +x $service_file
  $service_file
  redirect_to "$url"
fi
%>
<%in _header.cgi %>
<div class="row row-cols-1 row-cols-xl-2 g-3 mb-3">
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_vtun_1 %></div>
<div class="card-body">
<form action="<%= $url %>" method="post" autocomplete="off">
<%
if [ -f "$service_file" ]; then
  ex "cat $service_file"
  button_submit_action "reset" "$t_vtun_2" "data-method=\"delete\""
else
  extras=""; [ -n "$vtun_server" ] && extras=" disabled"
  field_text "vtun_server" "$extras"
  button_submit "$t_btn_submit" "primary"
fi
%>
</form>
</div>
</div>
</div>
</div>
<%in p/footer.cgi %>
