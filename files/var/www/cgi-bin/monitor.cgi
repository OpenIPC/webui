#!/usr/bin/haserl
content-type: text/html

<%in _header.cgi %>

<h3>Device Info</h3>
<pre><% echo "openipc-$(ipctool --chip_id)-$(ipctool --sensor_id | awk -F '_' '{print $1}')" %></pre>

<h3>Device Uptime</h3>
<pre><% /usr/bin/uptime %></pre>

<h3>Routing Table</h3>
<pre><% /bin/ip r %></pre>

<h3>Network Status</h3>
<pre><% /bin/ip a %></pre>

<h3>Ping Quality</h3>

<form action="/cgi-bin/update.cgi" method="POST">
<input type=hidden name="action" value="ping">
<input type="text" name="sense" pattern="^[a-zA-Z0-9-_.]+$" value="77.88.8.8" placeholder="FQDN or IP address" required>
<input type="radio" name="iface" value="auto" required checked="checked"> auto
<input type="radio" name="iface" value="eth0"> eth0
<input type="radio" name="iface" value="wlan0"> wlan0
<input type="submit" value="Run">
</form>

<h3>Trace Route</h3>
<form action="/cgi-bin/update.cgi" method="POST">
<input type=hidden name="action" value="trace">
<input type="text" name="sense" pattern="^[a-zA-Z0-9-_.]+$" value="77.88.8.8" placeholder="FQDN or IP address" required>
<input type="radio" name="iface" value="auto" required checked="checked"> auto
<input type="radio" name="iface" value="eth0"> eth0
<input type="radio" name="iface" value="wlan0"> wlan0
<input type="submit" value="Run">
</form>

<%in _footer.cgi %>
