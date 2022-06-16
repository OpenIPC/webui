#!/usr/bin/haserl
<%in _common.cgi %>
<%
plugin="vtun"
page_title="$tPageTitlePluginVtun"
service_file=/etc/init.d/S98vtun

if [ -n "$POST_action" ] && [ "$POST_action" = "reset" ]; then
  killall tunnel
  killall vtund
  rm $service_file
  redirect_to "/cgi-bin/plugin-vtun.cgi"
fi

if [ -n "$POST_vtun_server" ]; then
  echo -e "#!/bin/sh\n\ntunnel $POST_vtun_server" > $service_file
  chmod +x $service_file
  $service_file
  redirect_to "/cgi-bin/plugin-vtun.cgi"
fi
%>
<%in _header.cgi %>
<%
div_ "class=\"row row-cols-1 row-cols-xl-2 g-4 mb-3\""
  col_card_ "$tHeaderVtun"
    form_ "/cgi-bin/plugin-vtun.cgi" "post"
      if [ -f "$service_file" ]; then
        ex "cat $service_file"
        button_submit_action "reset" "$tButtonResetConfig" "data-method=\"delete\""
      else
        extras=""; [ -n "$vtun_server" ] && extras="${extras} disabled"
        field_text "vtun_server" "$extras"
        button_submit "$tButtonFormSubmit" "primary"
      fi
    _form
  _col_card
_div
%>
<%in _footer.cgi %>
