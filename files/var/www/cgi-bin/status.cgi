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
        <h5>Hardware</h5>
        <dl class="row">
          <dt class="col-4">SoC</dt>
          <dd class="col-8"><%= $soc %></dd>
          <dt class="col-4">SoC Family</dt>
          <dd class="col-8"><%= $soc_family %></dd>
          <dt class="col-4">Sensor</dt>
          <dd class="col-8"><%= $sensor %></dd>
          <dt class="col-4">Flash</dt>
          <dd class="col-8"><%= $flash_size %> MB</dd>
        <% if [ -n "$soc_temp" ]; then %>
          <dt class="col-4">SoC temp.</dt>
          <dd class="col-8"><%= $soc_temp %>°C</dd>
        <% fi %>
        </dl>
        <h5>Firmware</h5>
        <dl class="row">
          <dt class="col-4">Version</dt>
          <dd class="col-8"><%= $fw_version %>-<%= $fw_variant %></dd>
          <dt class="col-4">Build</dt>
          <dd class="col-8"><%= $fw_build %></dd>
        </dl>
        <dl class="row">
          <dt class="col-4">Hostname</dt>
          <dd class="col-8"><%= $hostname %></dd>
          <dt class="col-4">WAN MAC</dt>
          <dd class="col-8"><%= $wan_mac %></dd>
        </dl>
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
