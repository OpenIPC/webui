#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="Majestic config" %>
<%in p/header.cgi %>
<% ex "cat /etc/majestic.yaml" %>
<a class="btn btn-warning" href="texteditor.cgi?f=/etc/majestic.yaml">Edit file</a>
<%in p/footer.cgi %>
