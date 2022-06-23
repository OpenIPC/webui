#!/usr/bin/haserl
<%in p/common.cgi %>
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
<%in p/header.cgi %>
<div class="row row-cols-1 row-cols-xxl-3 g-4">
<div class="col">
<h3><%= $t_vtun_1 %></h3>
<form action="<%= $url %>" method="post">
<%
if [ -f "$service_file" ]; then
  ex "cat $service_file"
  action="reset"
  field_hidden "action"
  button_submit "$t_vtun_2"
else
  extras=""; [ -n "$vtun_server" ] && extras=" disabled"
  field_text "vtun_server" "$extras"
  button_submit
fi
%>
</form>
</div>
</div>
<%in p/footer.cgi %>
