#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_system_info
page_title="$tPageTitleNetworkAdministration"

network_hostname=$hostname

if [ "$(cat /etc/network/interfaces | grep "eth0 inet" | grep dhcp)" ]; then
  network_dhcp="true"
  disabled="disabled";
else
  network_dhcp="false"
  disabled="";
fi
network_ip_address=$(ifconfig eth0 | grep "inet " | tr ':' ' ' | awk '{print $3}')
network_netmask=$(ifconfig eth0 | grep "inet " | cut -d: -f4)
network_gateway=$(ip r | grep default | cut -d' ' -f3)
network_dns_1=$(cat /etc/resolv.conf | grep nameserver | sed -n 1p | cut -d' ' -f2)
network_dns_2=$(cat /etc/resolv.conf | grep nameserver | sed -n 2p | cut -d' ' -f2)
%>
<%in _header.cgi %>
<%
row_ "row-cols-1 row-cols-md-2 g-4 mb-4"
  col_card_ "$tHeaderSettings"
    form_ "/cgi-bin/network-update.cgi" "post"
      action="update"
      field_hidden "action"
      field_text "network_hostname" "data-pattern=\"host\""
      field_switch "network_dhcp"
      field_text "network_ip_address" "$disabled"
      field_text "network_netmask" "$disabled"
      field_text "network_gateway" "$disabled"
      field_text "network_dns_1" "$disabled"
      field_text "network_dns_2" "$disabled"
      button_submit "$tButtonFormSubmit" "primary"
    _form
  _col_card
_row

row_ "g-4 mb-4"
  col_card "$tHeaderNetworkInterfaces" "$(ex "cat /etc/network/interfaces")"
  col_card "$tHeaderNetworkAddress" "$(ex "ip address")"
  col_card "$tHeaderNetworkStatus" "$(ex "netstat -tulpan")"
  col_card "$tHeaderNetworkRouting" "$(ex "ip route list")"
  col_card "$tHeaderDnsResolver" "$(ex "cat /etc/resolv.conf")"
  col_card "$tHeaderNtpConfig" "$(ex "cat /etc/ntp.conf")"
_row
%>

<script>
$('#network_dhcp[type=checkbox]').addEventListener('change', (ev) => {
  $('#network_ip_address').disabled = ev.target.checked
  $('#network_netmask').disabled = ev.target.checked
  $('#network_gateway').disabled = ev.target.checked
  $('#network_dns_1').disabled = ev.target.checked
  $('#network_dns_2').disabled = ev.target.checked
});
</script>
<%in _footer.cgi %>
