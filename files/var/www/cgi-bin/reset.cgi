#!/usr/bin/haserl
<%in _header.cgi %>
<h2>Resetting Majestic configuration</h2>
<div class="alert alert-success mb-3 pre"><b># cp -v /rom/etc/majestic.yaml /etc/majestic.yaml</b><br>
<% echo "$(cp -v /rom/etc/majestic.yaml /etc/majestic.yaml 2>&1)" %></div>
<p><a href="/cgi-bin/majestic.cgi">Go to Majestic Settings</a></p>
<%in _footer.cgi %>
