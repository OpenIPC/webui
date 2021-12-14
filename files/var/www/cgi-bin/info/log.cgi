#!/usr/bin/haserl
<% page_title="logread" %>
<%in ../_common.cgi %>
<%in ../_header.cgi %>
<h2># logread</h2>
<pre><%= "$(logread | tail -100)" %></pre>
<a class="btn btn-primary  refresh">Refresh</a>
<%in ../_footer.cgi %>
