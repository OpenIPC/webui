#!/usr/bin/haserl
content-type: text/html

<%in _header.cgi %>
<% interfaces=$(/sbin/ifconfig | grep '^\w' | awk {'print $1'}) %>
<h2>Information</h2>

<div class="row row-cols-1 row-cols-xxl-2 g-4 mb-4">

<div class="col"><div class="card h-100 mb-3">
<h5 class="card-header">Device Info</h5>
<div class="card-body">
<h3 class="mb-3"><% echo "openipc-$(ipctool --chip_id)-$(ipctool --sensor_id | awk -F '_' '{print $1}')" %></h3>
<b># ipcinfo</b>
<pre>
Version: <%= $(cat /etc/os-release | grep "VERSION_ID" | cut -d= -f2) %>
SoC: <%= $(ipcinfo --chip_id) %>
Temperature: <%= $(ipcinfo --temp) %>°C
Sensor: <%= $(ipcinfo --long_sensor) %>
</pre>
</div></div></div>

<div class="col"><div class="card h-100 mb-3">
<h5 class="card-header">Network Status</h5>
<div class="card-body">
<b># netstat -tulpan</b>
<pre><% netstat -tulpan %></pre>
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
</div></div></div>

<div class="col"><div class="card h-100 mb-3">
<h5 class="card-header">Network Address</h5>
<div class="card-body">
<b># ip address</b>
<pre><% ip address %></pre>
</div></div></div>

<div class="col"><div class="card h-100 mb-3">
<h5 class="card-header">Network Routing</h5>
<div class="card-body">
<b># ip route list</b>
<pre><% ip route list %></pre>
</div></div></div>

</div>

<%in _footer.cgi %>
