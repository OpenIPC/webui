#!/usr/bin/haserl
<%in p/common.cgi %>
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
<%in p/header.cgi %>

<div class="row">
<div class="col col-md-6 col-lg-4 col-xxl-3">
<h3><%= $t_network_1 %></h3>
<form action="/cgi-bin/network-update.cgi" method="post">
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
button_submit
%>
</form>
</div>
<div class="col col-md-6 col-lg-8 col-xxl-9">
<h3><%= $t_network_5 %></h3>
<% ex "cat /etc/network/interfaces" %>
<h3><%= $t_network_6 %></h3>
<% ex "ip address" %>
<h3><%= $t_network_3 %></h3>
<% ex "ip route list" %>
<h3><%= $t_network_2 %></h3>
<% ex "cat /etc/resolv.conf" %>
<h3><%= $t_network_7 %></h3>
<% ex "netstat -tulpan" %>
</div>
</div>

<script>
function toggleDhcp() {
  const c = $('#network_dhcp[type=checkbox]').checked;
  $('#network_ip_address').disabled = c;
  $('#network_netmask').disabled = c;
  $('#network_gateway').disabled = c;
  $('#network_dns_1').disabled = c;
  $('#network_dns_2').disabled = c;
}
$('#network_dhcp[type=checkbox]').addEventListener('change', toggleDhcp);
toggleDhcp();
</script>
<%in p/footer.cgi %>
