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
<pre>
<%= $tSoC %>: <%= $soc %><br>
<%= $tSoCFamily %>: <%= $soc_family %><br>
<%= $tSensor %>: <%= $sensor %><br>
<%= $tFlash %>: <%= $flash_size %> MB<br>
<% if [ -n "$soc_temp" ]; then %><%= $tSoCTemp %>: <%= $soc_temp %>°C<% fi %><br>
</pre>
<b><%= $tFirmware %></b>
<pre>
<%= $tVersion %>: <%= $fw_version %>-<%= $fw_variant %><br>
<%= $tBuild %>: <%= $fw_build %><br>
</pre>
<b><%= $tSystem %></b>
<pre class="mb-0">
<%= $tHostname %>: <%= $hostname %><br>
<%= $tWanMac %>: <%= $wan_mac %><br>
</pre>
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
