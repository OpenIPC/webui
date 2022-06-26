#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="Majestic config" %>
<%in p/header.cgi %>
<%
f=/etc/majestic.yaml
ex "cat ${f}"
button_link_to "Edit file" "texteditor.cgi?f=${f}" "warning"
%>
<%in p/footer.cgi %>
