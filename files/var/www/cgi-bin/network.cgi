#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="network"
page_title="Network settings"

if [ "POST" = "$REQUEST_METHOD" ]; then

  tmp_file=/tmp/${plugin}.conf
  :> $tmp_file
  for v in address dhcp dns_1 dns_2 gateway hostname netmask; do
    eval echo "${plugin}_${v}=\\\"\$POST_${plugin}_${v}\\\"" >> $tmp_file
  done
  include $tmp_file

  for _i in hostname address netmask dateway dns_1 dns_2; do
    sanitize "network_${_i}"
  done; unset _i

  if [ "false" = "$network_dhcp" ]; then
    [ -z "$network_address" ] && error="IP address cannot be empty."
    [ -z "$network_netmask" ] && error="Networking mask cannot be empty."
    [ -z "$network_gateway" ] && error="Gateway IP address cannot be empty."
    [ -z "$network_dns_1" ] && error="Nameserver address cannot be empty."
    [ -z "$network_dns_2" ] && error="Nameserver address cannot be empty."
  fi

  [ -n "$error" ] && redirect_to $SCRIPT_NAME "danger" "$error"

  :> $tmp_file
  cat /etc/network/interfaces | sed '/^auto eth0$/,/^$/d' | sed -e :a -e '/^\n*$/{$d;N;};/\n$/ba' > $tmp_file
  if [ "$network_dhcp" = "true" ]; then
    echo "
auto eth0
iface eth0 inet dhcp
  hwaddress ether \$(fw_printenv -n ethaddr || echo 00:24:B8:FF:FF:FF)
" >> $tmp_file
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
" >> $tmp_file
    echo -e "nameserver ${network_dns_1}\nnameserver ${network_dns_2}" >/tmp/resolv.conf
  fi
  mv $tmp_file /etc/network/interfaces

  if [ -n "$network_hostname" ]; then
    if [ "$network_hostname" != "$hostname" ]; then
      echo "$network_hostname" > /etc/hostname
      hostname "$network_hostname"
#      sed -i 's/127.0.1.1.*${hostname}/127.0.1.1\t${network_hostname}/g' /etc/hosts
      sed -i "/127.0.1.1\s/s/^.*$/127.0.1.1\t${network_hostname}/" /etc/hosts # FIXME: hangs on update
      killall udhcpc
      udhcpc -x hostname:$network_hostname -T 1 -t 5 -R -b -O search
    fi
  fi

  update_caminfo
  touch /tmp/network-restart.txt
  redirect_to $SCRIPT_NAME
fi

[ -z "$network_hostname" ] && network_hostname=$hostname
[ -z "$network_dhcp" ] && network_dhcp=$dhcp
[ -z "$network_address" ] && network_address=$ipaddr
[ -z "$network_netmask" ] && network_netmask=$netmask
[ -z "$network_gateway" ] && network_gateway=$gateway
[ -z "$network_dns_1" ] && network_dns_1=$dns_1
[ -z "$network_dns_2" ] && network_dns_2=$dns_2
%>

<%in p/header.cgi %>

<div class="row">
  <div class="col col-md-6 col-lg-4 col-xxl-3">
    <h3>Settings</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "update" %>
      <% field_text "network_hostname" "Hostname" "Make hostname unique using MAC address information: ${macaddr}" %>
      <% field_switch "network_dhcp" "Use DHCP" %>
      <% field_text "network_address" "IP Address" %>
      <% field_text "network_netmask" "IP Netmask" %>
      <% field_text "network_gateway" "Gateway" %>
      <% field_text "network_dns_1" "DNS 1" %>
      <% field_text "network_dns_2" "DNS 2" %>
      <% button_submit %>
    </form>
  </div>
  <div class="col col-md-6 col-lg-8 col-xxl-9">
    <% ex "cat /etc/hostname" %>
    <% ex "cat /etc/hosts" %>
    <% ex "cat /etc/network/interfaces" %>
    <% ex "ip address" %>
    <% ex "ip route list" %>
    <% ex "cat /etc/resolv.conf" %>
    <% ex "netstat -tulpan" %>
  </div>
</div>

<script>
  function toggleDhcp() {
    const c = $('#network_dhcp[type=checkbox]').checked;
    $('#network_address').disabled = c;
    $('#network_netmask').disabled = c;
    $('#network_gateway').disabled = c;
    $('#network_dns_1').disabled = c;
    $('#network_dns_2').disabled = c;
  }

  $('#network_dhcp[type=checkbox]').addEventListener('change', toggleDhcp);

  toggleDhcp();
</script>

<%in p/footer.cgi %>
