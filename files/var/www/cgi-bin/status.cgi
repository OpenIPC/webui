#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="Device Status"
interfaces=$(/sbin/ifconfig | grep '^\w' | awk {'print $1'})
ipaddr=$(printenv | grep HTTP_HOST | cut -d= -f2 | cut -d: -f1)
hostname="Hostname: $(hostname -s)"

openipc_version=$(cat /etc/os-release | grep "OPENIPC_VERSION" | cut -d= -f2 2>&1)
openipc_build=$(cat /etc/os-release | grep "GITHUB_VERSION" | cut -d= -f2 | tr -d '"')
[ -n "$openipc_version" ] && openipc_version="<br>Version: ${openipc_version}"
[ -n "$openipc_build" ] && openipc_build="<br>Build: ${openipc_build}"
soc=$(ipcinfo --chip_id 2>&1)
[ -n "$soc" ] && soc="<br>SoC: ${soc}"
sensor=$(ipcinfo --long_sensor 2>&1)
[ -n "$sensor" ] && sensor="<br>Sensor: ${sensor}"
soc_temp=$(ipcinfo --temp 2>&1)
[ -n "$soc_temp" ] && soc_temp="<br>Temp.: $soc_temp°C"
wan_mac=$(cat /sys/class/net/*/address | grep -v 00:00:00:00:00:00 | head -1)
[ -n "$wan_mac" ] && wan_mac="<br>WAN MAC: ${wan_mac}"
%>
<%in _header.cgi %>
<div class="row">
  <div class="col mb-3">
    <div class="card h-100">
      <div class="card-header">Device Info</div>
      <div class="card-body">
        <b># ipcinfo</b>
        <pre><%= $hostname %><% echo -n "$openipc_version" %><% echo -n "$openipc_build" %><% echo -n "$soc" %><% echo -n "$sensor" %><% echo -n "$soc_temp" %><% echo -n "$wan_mac" %></pre>
      </div>
    </div>
  </div>

  <div class="col mb-3">
    <div class="card h-100">
      <div class="card-header">System Info</div>
      <div class="card-body">
        <b># date</b>
        <pre><% date %></pre>
        <p class="small">
          <a href="/cgi-bin/network-ntp.cgi">Edit timezone</a> |
          <a href="/cgi-bin/ntp-update.cgi">Sync time with an NTP server</a>
        </p>
        <b># uptime</b>
        <pre><% /usr/bin/uptime %></pre>
        <b># cat /proc/meminfo | grep Mem</b>
        <pre><% cat /proc/meminfo | grep Mem %></pre>
      </div>
    </div>
  </div>

  <div class="col mb-3">
    <div class="card h-100">
      <div class="card-header">Resources</div>
      <div class="card-body">
        <b># df</b>
        <pre><% df %></pre>
      </div>
    </div>
  </div>
</div>

<div class="row">
  <div class="col">
    <div class="card mb-3">
      <div class="card-header">Top 20 Processes</div>
      <div class="card-body">
        <pre><%= "$(ps aux | sort -nrk 3,3 | head -n 20)" %></pre>
      </div>
    </div>
  </div>
</div>

<%in _footer.cgi %>
