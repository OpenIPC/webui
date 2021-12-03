#!/usr/bin/haserl
content-type: text/html

<%in _header.cgi %>
<h2>Resetting Majestic configuration</h2>
<div class="alert alert-success mb-3 pre"><b># cp -v /rom/etc/majestic.yaml /etc/majestic.yaml</b><br>
<% echo "$(cp -v /rom/etc/majestic.yaml /etc/majestic.yaml 2>&1)" %></div>
<p><a href="/cgi-bin/index.cgi">Go back to settings</a></p>
<%in _footer.cgi %>
