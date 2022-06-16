#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleMajesticConfigCompare"
%>
<%in _header.cgi %>
<%
command="diff /rom/etc/majestic.yaml /etc/majestic.yaml"
output=$($command 2>&1)
# diff returns 0 on no difference, 1 on difference, 2+ on errors
# checking exit status won't work here
# checking for any output instead
if [ -z "$output" ]; then
  report_info "$tMsgNoChangesFound"
else
 report_command_info "$command" "$output"
fi

div_ "class=\"d-flex gap-2\""
  button_link_to "$tButtonDownloadConfig" "/cgi-bin/majestic-config-backup.cgi" "secondary"
  button_link_to "$tButtonDownloadAsPatch" "/cgi-bin/majestic-config-aspatch.cgi" "secondary"
  button_link_to "$tButtonRestoreConfig" "/cgi-bin/majestic-config-reset.cgi" "danger"
_div
%>
<%in _footer.cgi %>
