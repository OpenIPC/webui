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
div_ "class=\"row row-cols-1 row-cols-md-2 g-4 mb-4\""
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
      button_submit
    _form
  _col_card
_div

div_ "class=\"row g-4 mb-4\""
  col_card_ "$tHeaderNetworkInterfaces"
    b "# cat /etc/network/interfaces"
    pre "$(cat /etc/network/interfaces)"
  _col_card

  col_card_ "$tHeaderNetworkAddress"
    b "# ip address"
    pre "$(ip address | sed "s/</\&lt;/g" | sed "s/>/\&gt;/g")"
  _col_card

  col_card_ "$tHeaderNetworkRouting"
    b "# ip route list"
    pre "$(ip route list)"
  _col_card

  col_card_ "$tHeaderNetworkStatus"
    b "# netstat -tulpan"
    pre "$(netstat -tulpan)"
  _col_card

  col_card_ "$tHeaderDnsResolver"
    b "# cat /etc/resolv.conf"
    pre "$(cat /etc/resolv.conf 2>&1)"
  _col_card

  col_card_ "$tHeaderNtpConfig"
    b "# cat /etc/ntp.conf"
    pre "$(cat /etc/ntp.conf 2>&1)"
  _col_card

_div
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
