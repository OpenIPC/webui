#!/usr/bin/haserl
content-type: text/html

<%in _header.cgi %>
<% interfaces=$(/sbin/ifconfig | grep '^\w' | awk {'print $1'}) %>
<h2>Monitoring Tools</h2>

<div class="row row-cols-1 row-cols-xl-2 g-4 mb-4">

<div class="col"><div class="card h-100 mb-3">
<h5 class="card-header">Device Info</h5>
<div class="card-body">
<h3 class="mb-3"><% echo "openipc-$(ipctool --chip_id)-$(ipctool --sensor_id | awk -F '_' '{print $1}')" %></h3>
<b># ipcinfo</b>
<pre>
SoC: <%= $(ipcinfo --chip_id) %>
Temperature: <%= $(ipcinfo --temp) %>°C
Sensor: <%= $(ipcinfo --long_sensor) %>
</pre>
</div></div></div>

<div class="col"><div class="card h-100 mb-3">
<h5 class="card-header">OS Info</h5>
<div class="card-body">
<b># cat /etc/os-release</b>
<pre><% echo "$(cat /etc/os-release)" %></pre>
</div></div></div>

<div class="col"><div class="card h-100 mb-3">
<h5 class="card-header">Environment</h5>
<div class="card-body">
<b># date</b>
<pre><% date %></pre>
<b># uptime</b>
<pre><% /usr/bin/uptime %></pre>
<b># cat /proc/meminfo | grep Mem</b>
<pre><% cat /proc/meminfo | grep Mem %></pre>
<b># cat /proc/cpuinfo</b>
<pre><% cat /proc/cpuinfo %></pre>
 </div></div></div>

<div class="col"><div class="card h-100 mb-3">
<h5 class="card-header">Network</h5>
<div class="card-body">
<b># ip address</b>
<pre><% ip address %></pre>
<b># ip route list</b>
<pre><% ip route list %></pre>
<b># netstat -tu</b>
<pre><% netstat -tun %></pre>
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
<select name="iface">
<option>auto</option>
<% for i in $interfaces; do echo "<option>${i}</option>"; done %>
</select>
</div></div>
<p class="mb-0"><input type="submit" value="Run" class="btn btn-primary"></p>
</form></div></div></div>

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
<select name="iface">
<option>auto</option>
<% for i in $interfaces; do echo "<option>${i}</option>"; done %>
</select>
</div></div>
<p class="mb-0"><input type="submit" value="Run" class="btn btn-primary"></p>
</form></div></div></div>

</div>

<%in _footer.cgi %>
