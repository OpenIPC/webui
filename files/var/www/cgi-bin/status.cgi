#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="Device status" %>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <h3>Camera</h3>
    <h5>Hardware</h5>
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
    <h5>Firmware</h5>
    <dl class="small list">
      <dt>Version</dt>
      <dd><%= "${fw_version}-${fw_variant}" %></dd>
      <dt>Build</dt>
      <dd><%= $fw_build %></dd>
      <dt>Majestic</dt>
      <dd><%= $mj_version %></dd>
      <dt>Hostname</dt>
      <dd><%= $network_hostname %></dd>
    </dl>
  </div>

  <div class="col">
    <% ex "cat /etc/os-release" %>
  </div>
</div>

<div class="row g-4 mb-4 ui-expert">
  <div class="col ">
    <h3>Resources</h3>
    <% ex "/usr/bin/uptime" %>
    <% ex "df -T" %>
    <% ex "cat /proc/meminfo | grep Mem" %>
  </div>
</div>

<%in p/footer.cgi %>
