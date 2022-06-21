#!/usr/bin/haserl
<%in _common.cgi %>
<% page_title="$t_cron_0" %>
<%in _header.cgi %>
<%
f=/etc/crontabs/root
ex "cat ${f}"
button_link_to "$t_cron_1" "texteditor.cgi?f=${f}" "warning"
%>
<%in p/footer.cgi %>
