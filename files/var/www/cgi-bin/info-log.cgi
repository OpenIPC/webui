#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="Log read" %>
<%in p/header.cgi %>
<% ex "/sbin/logread" %>
<% button_refresh %>
<% button_download "logread" %>
<%in p/footer.cgi %>
