#!/usr/bin/haserl
content-type: text/html

<%in _header.cgi %>
<h2>Changes to Majestic config</h2>
<pre>
<% echo "$(diff /rom/etc/majestic.yaml /etc/majestic.yaml 2>&1)" %>
</pre>
<%in _footer.cgi %>
