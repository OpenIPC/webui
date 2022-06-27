#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="Diagnostic messages" %>
<%in p/header.cgi %>
<% ex "/bin/dmesg" %>
<a href="#" class="btn btn-primary refresh">Refresh</a>
<%in p/footer.cgi %>
