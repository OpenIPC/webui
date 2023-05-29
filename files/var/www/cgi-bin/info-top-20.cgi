#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="Top 20 Processes" %>
<%in p/header.cgi %>
<% ex "top -n 1 -b | sed '/top -n/d' | sed '1,4d' | head -20" %>
<%in p/footer.cgi %>
