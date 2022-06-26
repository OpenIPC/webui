#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="Cron settings" %>
<%in p/header.cgi %>
<%
f=/etc/crontabs/root
ex "cat ${f}"
button_link_to "Edit file" "texteditor.cgi?f=${f}" "warning"
%>
<%in p/footer.cgi %>
