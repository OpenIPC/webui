#!/usr/bin/haserl
<%
command="diff /rom/etc/majestic.yaml /etc/majestic.yaml"
output=$($command 2>&1)
result=$?
%>
<%in _header.cgi %>
<h2>Changes in Majestic config</h2>
<%
# diff returns 1 on success,
# checking exit status won't work here
# checking for any output instead
if [ -z "$output" ]; then %>
<pre>No changes found.</pre>
<% else %>
<div class="alert alert-info">
<pre>
<b># <%= $command %></b>
<%= "$output" %>
</pre>
</div>
<% fi %>
<p><a class="btn btn-primary" href="/cgi-bin/majestic.cgi">Go to Majestic settings page.</a>
   <a class="btn btn-danger" href="/cgi-bin/majestic-reset.cgi">Restore original configuration</a></p>
<%in _footer.cgi %>
