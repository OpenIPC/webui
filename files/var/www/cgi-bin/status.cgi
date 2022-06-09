#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_soc_temp
page_title="$tPageTitleDeviceStatus"
%>
<%in _header.cgi %>
<div class="row">

<% col_card_ "$tHeaderDeviceInfo" %>
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
</div></div></div>

<% col_card_ "$tHeaderSystemInfo" %>
<b># date</b>
<% pre "$(date)" %>
<p class="small">
<a href="/cgi-bin/network-ntp.cgi"><%= $tEditTimezone %></a> |
<a href="/cgi-bin/ntp-update.cgi"><%= $tSyncTime %></a>
</p>
<b># uptime</b>
<% pre "$(/usr/bin/uptime)" %>
<b># cat /proc/meminfo | grep Mem</b>
<% pre "$(cat /proc/meminfo | grep Mem)" %>
</div></div></div>

<% col_card_ "$tHeaderResources" %>
<b># df -T</b>
<% pre "$(df -T)" %>
</div></div></div>

</div>
<div class="row">

<% col_card_ "$tHeaderTopProcesses" %>
<b># top -n 1 -b | sed '/top -n/d' | sed '1,4d' | head -20</b>
<% pre "$(top -n 1 -b | sed '/top -n/d' | sed '1,4d' | head -20)" "class=\"mb-0\"" %>
</div></div></div>

</div>
<%in _footer.cgi %>
