#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_hardware_info
get_firmware_info
get_system_info
page_title=$tDeviceStatusTitle
%>
<%in _header.cgi %>
<div class="row">
<div class="col mb-3">
<div class="card h-100">
<div class="card-header"><%= $tDeviceInfoHeader %></div>
<div class="card-body">
<b><%= $tHardware %></b>
<pre><% echo "${tSoC}: ${soc}
${tSoCFamily}: ${soc_family}
${tSensor}: ${sensor}
${tFlash}: ${flash_size} MB"
[ -n "$soc_temp" ] && echo -n "${tSoCTemp}: ${soc_temp}°C"
%></pre>
<b><%= $tFirmware %></b>
<pre><% echo "${tVersion}: ${fw_version}-${fw_variant}
${tBuild}: ${fw_build}" %></pre>
<b><%= $tSystem %></b>
<pre><% echo "${tHostname}: ${hostname}
${tWanMac}: ${wan_mac}" %></pre>
</div>
</div>
</div>
  <div class="col mb-3">
    <div class="card h-100">
      <div class="card-header"><%= $tSystemInfoHeader %></div>
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
        <pre><% cat /proc/meminfo | grep Mem %></pre>
      </div>
    </div>
  </div>
  <div class="col mb-3">
    <div class="card h-100">
      <div class="card-header"><%= $tResourcesHeader %></div>
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
      <div class="card-header"><%= $tTopProcessesHeader %></div>
      <div class="card-body">
        <pre><%= "$(ps aux | sort -nrk 3,3 | head -n 20)" %></pre>
      </div>
    </div>
  </div>
</div>
<%in _footer.cgi %>
