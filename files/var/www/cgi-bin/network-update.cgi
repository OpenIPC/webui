#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="$t_networkup_0"

network_dhcp="$POST_network_dhcp"
network_hostname="$POST_network_hostname"
network_address="$POST_network_ip_address"
network_netmask="$POST_network_netmask"
network_gateway="$POST_network_gateway"
network_dns_1="$POST_network_dns_1"
network_dns_2="$POST_network_dns_2"

# strip trailing spaces
for _i in hostname address netmask dateway dns_1 dns_2; do
  sanitize "network_${_i}"
done; unset _i

if [ "false" = "$network_dhcp" ]; then
  [ -z "$network_address" ] && error="$t_networkup_1"
  [ -z "$network_netmask" ] && error="$t_networkup_2"
  [ -z "$network_gateway" ] && error="$t_networkup_3"
  [ -z "$network_dns_1" ] && error="$t_networkup_4"
  [ -z "$network_dns_2" ] && error="$t_networkup_5"
fi

if [ -n "$error" ]; then
  flash_save "danger" "$error"
  redirect_to "/cgi-bin/network.cgi"
fi

if [ -n "$network_hostname" ]; then
  if [ "$network_hostname" != "$hostname" ]; then
    echo "$network_hostname" > /etc/hostname
    hostname "$network_hostname"
    sed -i 's/127.0.1.1.*${hostname}/127.0.1.1\t${network_hostname}/g' /etc/hosts
    killall udhcpc
    udhcpc -x hostname:$network_hostname -T 1 -t 5 -R -b -O search
  fi
fi

tmp=/tmp/interfaces
cat /etc/network/interfaces | sed '/^auto eth0$/,/^$/d' | sed -e :a -e '/^\n*$/{$d;N;};/\n$/ba' > $tmp
if [ "$network_dhcp" = "true" ]; then
  echo "
auto eth0
iface eth0 inet dhcp
  hwaddress ether \$(fw_printenv -n ethaddr || echo 00:24:B8:FF:FF:FF)
" >> $tmp
else
  [ -z "$network_dns_2" ] && network_dns_2="$network_dns_1"
  echo "
auto eth0
iface eth0 inet static
  hwaddress ether \$(fw_printenv -n ethaddr || echo 00:24:B8:FF:FF:FF)
  address ${network_address}
  netmask ${network_netmask}
  gateway ${network_gateway}
  pre-up echo -e \"nameserver ${network_dns_1}\nnameserver ${network_dns_2}\n\" >/tmp/resolv.conf
" >> $tmp
  echo -e "nameserver ${network_dns_1}\nnameserver ${network_dns_2}" >/tmp/resolv.conf
fi
mv $tmp /etc/network/interfaces
update_caminfo
%>
<%in p/header.cgi %>
<%
alert_ "danger"
  h6 "$t_networkup_6"
  p "$t_networkup_7"
  button_reboot
_alert
link_to "$t_networkup_9" "/cgi-bin/network.cgi"
%>
<%in p/footer.cgi %>
