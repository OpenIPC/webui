#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="Cron settings" %>
<%in p/header.cgi %>
<% ex "cat /etc/crontabs/root" %>
<a class="btn btn-warning" href="texteditor.cgi?f=/etc/crontabs/root">Edit file</a>
<%in p/footer.cgi %>
