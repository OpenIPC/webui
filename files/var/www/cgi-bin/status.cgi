#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_soc_temp
page_title="$tPageTitleDeviceStatus"
%>
<%in _header.cgi %>
<div class="row">
  <div class="col mb-3">
    <div class="card h-100">
      <div class="card-header"><%= $tHeaderDeviceInfo %></div>
      <div class="card-body">
        <b><%= $tHardware %></b>
        <pre><%
        print2c "${tSoC}:" "${soc}"
        print2c "${tSoCFamily}:" "${soc_family}"
        print2c "${tSensor}:" "${sensor_ini}"
        print2c "${tFlash}:" "${flash_size} MB"
        [ -n "$soc_temp" ] && print2c "${tSoCTemp}:" "${soc_temp}°C"
        %></pre>
        <b><%= $tFirmware %></b>
        <pre><%
        print2c "${tVersion}:" "${fw_version}-${fw_variant}"
        print2c "${tBuild}:" "${fw_build}"
        %></pre>
        <b><%= $tSystem %></b>
        <pre class="mb-0"><%
        print2c "${tHostname}:" "${hostname}"
        print2c "${tWanMac}:" "${wan_mac}"
        %></pre>
      </div>
    </div>
  </div>
  <div class="col mb-3">
    <div class="card h-100">
      <div class="card-header"><%= $tHeaderSystemInfo %></div>
      <div class="card-body">
        <b># date</b>
        <pre><% date %></pre>
        <p class="small">
        <a href="/cgi-bin/network-ntp.cgi"><%= $tEditTimezone %></a> |
        <a href="/cgi-bin/ntp-update.cgi"><%= $tSyncTime %></a>
        </p>
        <b># uptime</b>
        <pre><% /usr/bin/uptime %></pre>
        <b># cat /proc/meminfo | grep Mem</b>
        <pre class="mb-0"><% cat /proc/meminfo | grep Mem %></pre>
      </div>
    </div>
  </div>
  <div class="col mb-3">
    <div class="card h-100">
      <div class="card-header"><%= $tHeaderResources %></div>
      <div class="card-body">
        <b># df -T</b>
        <pre class="mb-0"><% df -T %></pre>
      </div>
    </div>
  </div>
</div>
<div class="row">
  <div class="col">
    <div class="card mb-3">
      <div class="card-header"><%= $tHeaderTopProcesses %></div>
      <div class="card-body">
        <b># top -n 1 -b | sed '/top -n/d' | sed '1,4d' | head -20</b>
        <pre class="mb-0"><%= "$(top -n 1 -b | sed '/top -n/d' | sed '1,4d' | head -20)" %></pre>
      </div>
    </div>
  </div>
</div>
<%in _footer.cgi %>
