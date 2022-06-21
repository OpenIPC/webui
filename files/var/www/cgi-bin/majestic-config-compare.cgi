#!/usr/bin/haserl
<%in _common.cgi %>
<% page_title="$t_mjcompare_0" %>
<%in _header.cgi %>
<%
_c="diff /rom/etc/majestic.yaml /etc/majestic.yaml"
_o=$($_c 2>&1)
# diff returns 0 on no difference, 1 on difference, 2+ on errors. exit status won't work here. checking for any output instead
if [ -z "$_o" ]; then
report_info "$t_mjcompare_1"
else
report_command_info "$_c" "$_o"
fi

div_ "d-flex gap-2"
button_link_to "$t_mjcompare_2" "/cgi-bin/majestic-config-backup.cgi" "secondary"
button_link_to "$t_mjcompare_3" "/cgi-bin/majestic-config-aspatch.cgi" "secondary"
button_link_to "$t_mjcompare_4" "/cgi-bin/majestic-config-reset.cgi" "danger"
_div
%>
<%in p/footer.cgi %>
