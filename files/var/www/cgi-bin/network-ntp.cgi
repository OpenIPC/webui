#!/usr/bin/haserl
<%in _common.cgi %>
<% page_title="$t_ntp_0" %>
<%in _header.cgi %>
<% if [ "$(cat /etc/TZ)" != "$TZ" ]; then %>
<div class="alert alert-danger">
<h6><%= $t_ntp_1 %></h6>
<p><%= $t_ntp_2 %></p>
<% button_reboot %>
</div>
<% fi %>
<div class="row row-cols-1 row-cols-md-2 g-3 mb-3">
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_ntp_4 %></div>
<div class="card-body">
<form action="/cgi-bin/network-tz-update.cgi" method="post" autocomplete="off">
<div class="mb-2 string">
<label for="tz_name" class="form-label"><%= $tL_tz_name %></label>
<div class="input-group">
<input type="text" name="tz_name" id="tz_name" value="<%= $tz_name %>" class="form-control" list="tz_list">
<datalist id="tz_list"></datalist>
</div>
<p class="hint text-secondary"><%= $tH_tz_name1 %> (<a href="#" id="frombrowser"><%= $tH_tz_name2 %></a>)</p>
</div>
<div class="mb-2 string">
<label for="tz_data" class="form-label"><%= $tL_tz_data %></label>
<div class="input-group">
<input type="text" name="tz_data" id="tz_data" value="<%= $tz_data %>" class=" form-control" readonly>
</div>
<p class="hint text-secondary"><%= $tH_tz_data %></p>
</div>
<button type="submit" class="btn btn-primary mt-3"><%= $t_btn_submit %></button>
</form>
</div>
</div>
</div>
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_ntp_5 %></div>
<div class="card-body">
<%
ex "cat /etc/TZ"
ex "cat /etc/tz_name"
ex "echo \$TZ"
ex "/bin/date"
%>
</div>
</div>
</div>
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_ntp_6 %></div>
<div class="card-body">
<form action="/cgi-bin/network-ntp-update.cgi" method="post" autocomplete="off">
<%
for i in 0 1 2 3; do
  x=$(expr $i + 1)
  eval "ntp_server_${i}=$(sed -n ${x}p /etc/ntp.conf | cut -d' ' -f2)"
%>
<div class="mb-2 string">
<label class="form-label" for="ntp_server_<%= $i %>"><% eval echo \$tL_ntp_server_${i} %></label>
<input type="text" class="form-control" id="ntp_server_<%= $i %>" name="ntp_server_<%= $i %>" placeholder="<%= $i %>.pool.ntp.org" data-pattern="host-ip" value="<% eval echo \$ntp_server_${i} %>">
</div>
<% done %>
<button type="submit" class="btn btn-primary mt-3"><%= $t_btn_submit %></button>
</form>
</div>
</div>
</div>
<div class="col ">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_ntp_7 %></div>
<div class="card-body">
<% ex "cat /etc/ntp.conf" %>
<a class="btn btn-danger" href="/cgi-bin/network-ntp-reset.cgi"><%= $t_ntp_8 %></a>
</div>
</div>
</div>
</div>
<script src="/a/tz.js"></script>
<%in p/footer.cgi %>
