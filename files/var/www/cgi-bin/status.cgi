#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_hardware_info
get_firmware_info
get_system_info
page_title="Device Status"
%>
<%in _header.cgi %>
<div class="row">
<div class="col mb-3">
<div class="card h-100">
<div class="card-header">Device Info</div>
<div class="card-body">
<b>Hardware</b>
<pre>
SoC           <%= $soc %>
SoC Family    <%= $soc_family %>
Sensor        <%= $sensor %>
Flash         <%= $flash_size %> MB
<% if [ -n "$soc_temp" ]; then %>SoC temp.     <%= $soc_temp %>°C<% fi %>
</pre>
<b>Firmware</b>
<pre>
Version       <%= $fw_version %>-<%= $fw_variant %>
Build         <%= $fw_build %>
</pre>
<b>System</b>
<pre class="mb-0">
Hostname      <%= $hostname %></dd>
WAN MAC       <%= $wan_mac %>
</pre>
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
