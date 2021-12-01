#!/usr/bin/haserl
content-type: text/html

<%in _header.cgi %>

<h3>Device Info</h3>
<pre><% echo "openipc-$(ipctool --chip_id)-$(ipctool --sensor_id | awk -F '_' '{print $1}')" %></pre>

<h3>Device Uptime</h3>
<pre><% /usr/bin/uptime %></pre>

<h3>Routing Table</h3>
<pre><% ip r %></pre>

<h3>Network Status</h3>
<pre><% ip a %></pre>

<h3>Ping Quality</h3>
<form action="/cgi-bin/update.cgi" method="post">
<input type=hidden name="action" value="ping">
<dl>
<dt>Target FQDN or IP address</dt>
<dd><input type="text" name="target" pattern="^[a-zA-Z0-9-_.]+$" value="4.2.2.1"
  placeholder="FQDN or IP address" required></dd>
<dt>Use network interface</dt>
<dd>
<input type="radio" name="iface" value="auto" required checked="checked"> auto
<input type="radio" name="iface" value="eth0"> eth0
<input type="radio" name="iface" value="wlan0"> wlan0
</dd>
</dl>
<p><input type="submit" value="Run"></p>
</form>

<h3>Trace Route</h3>
<form action="/cgi-bin/update.cgi" method="post">
<input type=hidden name="action" value="trace">
<dl>
<dt>Target FQDN or IP address</dt>
<dd><input type="text" name="target" pattern="^[a-zA-Z0-9-_.]+$" value="4.2.2.1"
  placeholder="FQDN or IP address" required></dd>
<dt>Use network interface</dt>
<dd>
<input type="radio" name="iface" value="auto" required checked="checked"> auto
<input type="radio" name="iface" value="eth0"> eth0
<input type="radio" name="iface" value="wlan0"> wlan0
</dd>
</dl>
<p><input type="submit" value="Run"></p>
</form>

<%in _footer.cgi %>
