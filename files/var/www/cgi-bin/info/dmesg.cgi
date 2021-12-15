#!/usr/bin/haserl
<% page_title="dmesg" %>
<%in ../_common.cgi %>
<%in ../_header.cgi %>
<h2># dmesg</h2>
<pre class="bg-light p-4"><%= "$(dmesg)" %></pre>
<a class="btn btn-primary refresh">Refresh</a>
<%in ../_footer.cgi %>
