#!/usr/bin/haserl
content-type: text/html

<%
interfaces=$(/sbin/ifconfig | grep '^\w' | awk {'print $1'})
ipaddr=$(printenv | grep HTTP_HOST | cut -d= -f2 | cut -d: -f1)
top=$(top -n1)
%>
<%in _header.cgi %>
<h2>Camera Information and Status</h2>

<div class="row">
  <div class="col mb-3">
    <div class="card h-100">
      <div class="card-header">Device Info</div>
      <div class="card-body">
        <h3 class="mb-3"><% echo "openipc-$(ipctool --chip_id)-$(ipctool --sensor_id | awk -F '_' '{print $1}')" %></h3>
        <b># ipcinfo</b>
        <pre>Version: <%= $(cat /etc/os-release | grep "OPENIPC_VERSION" | cut -d= -f2) %>
SoC: <%= $(ipcinfo --chip_id) %>
Temperature: <%= $(ipcinfo --temp) %>°C
Sensor: <%= $(ipcinfo --long_sensor) %></pre>
      </div>
    </div>
  </div>

  <div class="col mb-3">
    <div class="card h-100">
      <div class="card-header">System Info</div>
      <div class="card-body">
        <b># uptime</b>
        <pre><% /usr/bin/uptime %></pre>
        <b># cat /proc/meminfo | grep Mem</b>
        <pre><% cat /proc/meminfo | grep Mem %></pre>
      </div>
    </div>
  </div>
</div>

<div class="row">
  <div class="col">
    <div class="card mb-3">
      <div class="card-header">Top Processes</div>
      <div class="card-body">
        <pre><%= "$(echo "$top" | sed 's/\x1b\[[0-9;]*[a-zA-Z]//g')" %></pre>
      </div>
    </div>
  </div>
</div>

<%in _footer.cgi %>
