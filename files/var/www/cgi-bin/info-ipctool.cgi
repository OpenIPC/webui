#!/usr/bin/haserl
<%in p/common.cgi %>
<%
actions="info i2cdetect reginfo"
action=$GET_action
if [ -z "$action" ]; then
  action=$(echo $actions | awk '{print $1}')
  redirect_to "${SCRIPT_NAME}?action=${action}"
fi
command="ipctool"
page_title="IPC Tool"
if [ "$action" = "info" ]; then
  command="${command}"
  page_title="${page_title}: Camera Information"
else
  command="${command} ${action}"
  page_title="${page_title}: ${action}"
fi
# ipctool i2cdump 0x78 0x0 0x3ff
%>
<%in p/header.cgi %>
<p><%
for c in $actions; do
  css="btn btn-sm btn-primary"
  [ "$c" = "$action" ] && css="${css} active"
  echo "<a class=\"${css}\" href=\"${SCRIPT_NAME}?action=${c}\">${c}</a>"
done
%>
</p>
<% ex "${command}" %>
<% button_refresh %>
<%in p/footer.cgi %>
