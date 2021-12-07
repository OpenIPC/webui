#!/usr/bin/haserl
content-type: text/html

<%
result=$(diff /rom/etc/majestic.yaml /etc/majestic.yaml 2>&1)
%>
<%in _header.cgi %>
<h2>Changes in Majestic config</h2>
<% if [ -z "$result" ]; then %>
<pre>No changes found.</pre>
<% else %>
<div class="alert alert-info">
<pre><% echo "$result" %></pre>
</div>
<% fi %>
<p><a href="/cgi-bin/majestic.cgi">Go to Majestic settings page.</a></p>
<%in _footer.cgi %>
