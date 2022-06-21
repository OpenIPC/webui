#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_soc_temp
page_title="$t_status_0"
%>
<%in _header.cgi %>
<div class="row row-cols-1 row-cols-lg-2 g-3 mb-3">
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_status_1 %></div>
<div class="card-body">
<b><%= $t_status_2 %></b>
<pre class="small">
<span class="title"><%= $t_status_3 %></span> <span><%= $soc %></span>
<span class="title"><%= $t_status_4 %></span> <span><%= $soc_family %></span>
<span class="title"><%= $t_status_5 %></span> <span><%= $sensor_ini %></span>
<span class="title"><%= $t_status_6 %></span> <span><%= $flash_size %> MB</span>
</pre>
<!--[ -n "$soc_temp" ] && e2c "$tSoCTemp" "${soc_temp}°C"-->
<b><%= $t_status_7 %></b>
<pre class="small">
<span class="title"><%= $t_status_8 %></span> <span><%= "${fw_version}-${fw_variant}" %></span>
<span class="title"><%= $t_status_9 %></span> <span><%= $fw_build %></span>
</pre>
<b><%= $t_status_a %></b>
<pre class="small mb-0">
<span class="title"><%= $t_status_b %></span> <span><%= $hostname %></span>
<span class="title"><%= $t_status_c %></span> <span><%= $wan_mac %></span>
</pre>
</div>
</div>
</div>
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_status_d %></div>
<div class="card-body">
<% ex "/bin/date" %>
<div class="small mb-3">
<a href="/cgi-bin/network-ntp.cgi" class="me-2" ><%= $t_status_e %></a>
<a href="/cgi-bin/ntp-update.cgi"><%= $t_status_f %></a>
</div>
<% ex "/usr/bin/uptime" %>
<% ex "cat /proc/meminfo | grep Mem" %>
</div>
</div>
</div>
</div>
<div class="row row-cols-1 g-3 mb-3">
<div class="col ">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_status_g %></div>
<div class="card-body">
<% ex "df -T" %>
</div>
</div>
</div>
</div>
<div class="row row-cols-1 g-3 mb-3">
<div class="col ">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_status_h %></div>
<div class="card-body">
<% ex "top -n 1 -b | sed '/top -n/d' | sed '1,4d' | head -20" %>
</div>
</div>
</div>
</div>
<%in p/footer.cgi %>
