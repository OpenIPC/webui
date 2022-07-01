#!/usr/bin/haserl
<%in p/common.cgi %>
<%
get_soc_temp
page_title="Device status"
%>
<%in p/header.cgi %>

<div class="row row-cols-lg-3 g-4">
  <div class="col">
    <h3>Camera</h3>
    <h4>Hardware</h4>
    <dl class="small list">
      <dt>Processor</dt>
      <dd><%= $soc %></dd>
      <dt>Family</dt>
      <dd><%= $soc_family %></dd>
      <dt>Sensor</dt>
      <dd><%= $sensor_ini %></dd>
      <dt>Flash</dt>
      <dd><%= $flash_size %> MB</dd>
    </dl>
  </div>
  <div class="col">
    <h3>System</h3>
    <h4>Firmware</h4>
    <dl class="small list">
      <dt>Version</dt>
      <dd><%= "${fw_version}-${fw_variant}" %></dd>
      <dt>Build</dt>
      <dd><%= $fw_build %></dd>
      <dt>Hostname</dt>
      <dd><%= $network_hostname %></dd>
      <dt>WAN MAC</dt>
      <dd><%= $network_wan_mac %></dd>
    </dl>
  </div>
  <div class="col">
    <h3>Date & Time</h3>
    <% ex "/bin/date" %>
    <div class="d-flex gap-2 mx-auto">
      <a href="network-ntp.cgi" class="btn btn-primary">Edit timezone</a>
      <a href="ntp-update.cgi" class="btn btn-primary">Syncronize time</a>
    </div>
  </div>
</div>
<div class="row g-4">
  <div class="col ">
    <h3>Resources</h3>
    <% ex "/usr/bin/uptime" %>
    <% ex "df -T" %>
    <% ex "cat /proc/meminfo | grep Mem" %>
  </div>
  <div class="col">
    <h3>Top 20 Processes</h3>
    <% ex "top -n 1 -b | sed '/top -n/d' | sed '1,4d' | head -20" %>
  </div>
</div>

<%in p/footer.cgi %>
