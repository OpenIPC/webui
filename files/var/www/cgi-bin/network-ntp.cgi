#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="$t_ntp_0" %>
<%in p/header.cgi %>
<% if [ "$(cat /etc/TZ)" != "$TZ" ]; then %>
<div class="alert alert-danger">
<h4><%= $t_ntp_1 %></h4>
<p><%= $t_ntp_2 %></p>
<% button_reboot %>
</div>
<% fi %>
<div class="row row-cols-1 row-cols-md-2 row-cols-xxl-4 g-4">
<div class="col">
<h3><%= $t_ntp_4 %></h3>
<p><a href="#" id="frombrowser"><%= $tH_tz_name2 %></a></p>
<form action="/cgi-bin/network-tz-update.cgi" method="post">
<datalist id="tz_list"></datalist>
<%
field_text "tz_name" "" "list=tz_list"
field_text "tz_data" "" "readonly"
button_submit
%>
</form>
</div>
<div class="col">
<h3><%= $t_ntp_5 %></h3>
<%
ex "cat /etc/TZ"
ex "cat /etc/tz_name"
ex "echo \$TZ"
ex "/bin/date"
%>
</div>
<div class="col">
<h3><%= $t_ntp_6 %></h3>
<form action="/cgi-bin/network-ntp-update.cgi" method="post">
<%
for i in 0 1 2 3; do
  x=$(expr $i + 1)
  eval "ntp_server_${i}=$(sed -n ${x}p /etc/ntp.conf | cut -d' ' -f2)"
  field_text "ntp_server_${i}"
done
button_submit
%>
</form>
</div>
<div class="col">
<h3><%= $t_ntp_7 %></h3>
<% ex "cat /etc/ntp.conf" %>
<a class="btn btn-danger" href="/cgi-bin/network-ntp-reset.cgi"><%= $t_ntp_8 %></a>
</div>
</div>

<script src="/a/tz.js"></script>
<%in p/footer.cgi %>
