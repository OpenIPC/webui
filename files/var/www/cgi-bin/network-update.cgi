#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleNetworkUpdate"

dhcp="$POST_network_dhcp"
hostname="$POST_network_hostname"
address="$POST_network_ip_address"
netmask="$POST_network_netmask"
gateway="$POST_network_gateway"
dns1="$POST_network_dns_1"
dns2="$POST_network_dns_2"

if [ "$dhcp" == "false" ]; then
  [ -z "$address" ] && error="IP address cannot be empty."
  [ -z "$netmask" ] && error="Networking mask cannot be empty."
  [ -z "$gateway" ] && error="Gateway IP address cannot be empty."
  [ -z "$dns1" ] && error="Nameserver address cannot be empty."
  [ -z "$dns2" ] && error="Nameserver address cannot be empty."
fi

if [ -n "$error" ]; then
  flash_save "danger" "$error"
  redirect_to "/cgi-bin/network.cgi"
fi

if [ -n "$hostname" ]; then
  oldhostname=$(cat /etc/hostname)
  if [ "$hostname" != "$oldhostname" ]; then
    echo "$hostname" > /etc/hostname
    hostname "$hostname"
    sed -i 's/127.0.1.1.*${oldhostname}/127.0.1.1\t${POST_hostname}/g' /etc/hosts
    killall udhcpc
    udhcpc -x hostname:$hostname -T 1 -t 5 -R -b -O search
  fi
fi

tmp=/tmp/interfaces
cat /etc/network/interfaces | sed '/^auto eth0$/,/^$/d' | sed -e :a -e '/^\n*$/{$d;N;};/\n$/ba' > "$tmp"
if [ "$dhcp" = "true" ]; then
  echo "
auto eth0
iface eth0 inet dhcp
  hwaddress ether \$(fw_printenv -n ethaddr || echo 00:24:B8:FF:FF:FF)
" >> "$tmp"
else
  [ -z "$dns2" ] && dns2="$dns1"
  echo "
auto eth0
iface eth0 inet static
  hwaddress ether \$(fw_printenv -n ethaddr || echo 00:24:B8:FF:FF:FF)
  address ${address}
  netmask ${netmask}
  gateway ${gateway}
  pre-up echo -e \"nameserver ${dns1}\nnameserver ${dns2}\n\" >/tmp/resolv.conf
" >> "$tmp"
  echo -e "nameserver ${dns1}\nnameserver ${dns2}" >/tmp/resolv.conf
fi
mv "$tmp" /etc/network/interfaces
%>
<%in _header.cgi %>
<%
alert_ "danger"
  h6 "$tMsgNetworkUpdated"
  p "$tMsgRestartNeeded"
  button_link_to "$tButtonReboot" "/cgi-bin/reboot.cgi" "danger"
_alert
link_to "$tButtonGoBackToSettings" "/cgi-bin/network.cgi"
%>
<%in _footer.cgi %>
