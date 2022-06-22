#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$t_network_0"

network_dhcp="$dhcp"
network_hostname="$hostname"
network_ip_address="$ipaddr"
network_netmask="$netmask"
network_gateway="$gateway"
network_dns_1="$dns_1"
network_dns_2="$dns_2"
%>
<%in _header.cgi %>

<div class="row mb-3">
<div class="col-md-6 col-lg-4">
<div class="card">
<div class="card-header"><%= $t_network_1 %></div>
<div class="card-body">
<form action="/cgi-bin/network-update.cgi" method="post" autocomplete="off">
<%
action="update"
field_hidden "action"
field_text "network_hostname" "data-pattern=host"
field_switch "network_dhcp"
field_text "network_ip_address"
field_text "network_netmask"
field_text "network_gateway"
field_text "network_dns_1"
field_text "network_dns_2"
%>
<button type="submit" class="btn btn-primary mt-3"><%= $t_btn_submit %></button>
</form>
</div>
</div>
</div>
<div class="col-md-6 col-lg-8">
<div class="row row-cols-1 g-3">
<%
col_card "$t_network_2" "$(ex "cat /etc/resolv.conf")"
col_card "$t_network_3" "$(ex "ip route list")"
col_card "$t_network_4" "$(ex "cat /etc/ntp.conf")"
%>
</div>
</div>
</div>

<div class="row row-cols-1 g-3 mb-3">
<%
col_card "$t_network_5" "$(ex "cat /etc/network/interfaces")"
col_card "$t_network_6" "$(ex "ip address")"
col_card "$t_network_7" "$(ex "netstat -tulpan")"
%>
</div>

<script>
function toggleDhcp() {
  $('#network_ip_address').disabled = $('#network_netmask').disabled = $('#network_gateway').disabled = $('#network_dns_1').disabled = $('#network_dns_2').disabled = $('#network_dhcp[type=checkbox]').checked;
}
$('#network_dhcp[type=checkbox]').addEventListener('change', toggleDhcp);
toggleDhcp();
</script>
<%in p/footer.cgi %>
