#!/usr/bin/haserl
content-type: text/html

<%in _header.cgi %>

<h2>Monitoring Tools</h2>

<div class="row row-cols-1 row-cols-xl-2 g-4 mb-4">

<div class="col"><div class="card h-100 mb-3">
<h5 class="card-header">Device Info</h5>
<div class="card-body">
<pre><% echo "openipc-$(ipctool --chip_id)-$(ipctool --sensor_id | awk -F '_' '{print $1}')" %></pre>
</div></div></div>

<div class="col"><div class="card h-100 mb-3">
<h5 class="card-header">Device Uptime</h5>
<div class="card-body">
<pre><% /usr/bin/uptime %></pre>
</div></div></div>

<div class="col"><div class="card h-100 mb-3">
<h5 class="card-header">Routing Table</h5>
<div class="card-body">
<pre><% ip r %></pre>
</div></div></div>

<div class="col"><div class="card h-100 mb-3">
<h5 class="card-header">Network Status</h5>
<div class="card-body">
<pre><% ip a %></pre>
</div></div></div>

<div class="col"><div class="card h-100 mb-3">
<h5 class="card-header">Ping Quality</h5>
<div class="card-body">
<form action="/cgi-bin/tools.cgi" method="post">
<input type=hidden name="action" value="ping">
<div class="row mb-3">
<div class="col-md-6"><label for="target">Target FQDN or IP address</label></div>
<div class="col-md-6"><input type="text" name="target" pattern="^[a-zA-Z0-9-_.]+$" value="4.2.2.1" placeholder="FQDN or IP address" required></div>
</div>
<div class="row mb-3">
<div class="col-md-6"><label for="iface">Use network interface</label></div>
<div class="col-md-6">
<input type="radio" name="iface" value="auto" checked="checked"> auto
<input type="radio" name="iface" value="eth0"> eth0
<input type="radio" name="iface" value="wlan0"> wlan0
</div>
</div>
<p class="mb-0"><input type="submit" value="Run" class="btn btn-primary"></p>
</form>
</div></div></div>

<div class="col"><div class="card h-100 mb-3">
<h5 class="card-header">Trace Route</h5>
<div class="card-body">
<form action="/cgi-bin/tools.cgi" method="post">
<input type=hidden name="action" value="trace">
<div class="row mb-3">
<div class="col-md-6"><label for="">Target FQDN or IP address</label></div>
<div class="col-md-6"><input type="text" name="target" pattern="^[a-zA-Z0-9-_.]+$" value="4.2.2.1" placeholder="FQDN or IP address" required></div>
</div>
<div class="row mb-3">
<div class="col-md-6"><label for="">Use network interface</label></div>
<div class="col-md-6">
<input type="radio" name="iface" value="auto" checked="checked"> auto
<input type="radio" name="iface" value="eth0"> eth0
<input type="radio" name="iface" value="wlan0"> wlan0
</div></div>
<p class="mb-0"><input type="submit" value="Run" class="btn btn-primary"></p>
</form>
</div></div></div>

</div>

<%in _footer.cgi %>
