#!/usr/bin/haserl
<%in p/common.cgi %>
<%
get_soc_temp
page_title="$t_status_0"
%>
<%in p/header.cgi %>

<div class="row g-4">
  <div class="col">
    <h3><%= $t_status_1 %></h3>
    <h4><%= $t_status_2 %></h4>
    <dl class="small list">
      <dt><%= $t_status_3 %></dt><dd><%= $soc %></dd>
      <dt><%= $t_status_4 %></dt><dd><%= $soc_family %></dd>
      <dt><%= $t_status_5 %></dt><dd><%= $sensor_ini %></dd>
      <dt><%= $t_status_6 %></dt><dd><%= $flash_size %> MB</dd>
    </dl>
    <!--[ -n "$soc_temp" ] && echo "<b>${tSoCTemp}</b> ${soc_temp}°C"-->
  </div>
  <div class="col">
    <h3><%= $t_status_d %></h3>
    <h4><%= $t_status_7 %></h4>
    <dl class="small list">
      <dt><%= $t_status_8 %></dt><dd><%= "${fw_version}-${fw_variant}" %></dd>
      <dt><%= $t_status_9 %></dt><dd><%= $fw_build %></dd>
      <dt><%= $t_status_b %></dt><dd><%= $hostname %></dd>
      <dt><%= $t_status_c %></dt><dd><%= $wan_mac %></dd>
    </dl>
  </div>
  <div class="col">
    <h3><%= $t_status_a %></h3>
    <% ex "/bin/date" %>
    <div class="d-flex gap-2 mx-auto">
      <a href="/cgi-bin/network-ntp.cgi" class="btn btn-primary"><%= $t_status_e %></a>
      <a href="/cgi-bin/ntp-update.cgi" class="btn btn-primary"><%= $t_status_f %></a>
    </div>
  </div>
</div>

<div class="row g-4">
  <div class="col ">
    <h3><%= $t_status_g %></h3>
    <% ex "/usr/bin/uptime" %>
    <% ex "df -T" %>
    <% ex "cat /proc/meminfo | grep Mem" %>
  </div>
  <div class="col">
    <h3><%= $t_status_h %></h3>
    <% ex "top -n 1 -b | sed '/top -n/d' | sed '1,4d' | head -20" %>
  </div>
</div>

<%in p/footer.cgi %>
