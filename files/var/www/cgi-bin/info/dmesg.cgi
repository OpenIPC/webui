#!/usr/bin/haserl
<% page_title="dmesg" %>
<%in ../_common.cgi %>
<%in ../_header.cgi %>
<h2># dmesg</h2>
<pre><%= "$(dmesg)" %></pre>
<a class="btn btn-primary refresh">Refresh</a>
<%in ../_footer.cgi %>
