#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="network"
page_title="Network settings"
params="address dhcp dns_1 dns_2 gateway hostname netmask"
tmp_file=/tmp/${plugin}.conf

if [ "POST" = "$REQUEST_METHOD" ]; then
  # parse values from parameters
  for _p in $params; do
    eval ${plugin}_${_p}=\$POST_${plugin}_${_p}
    sanitize "${plugin}_${_p}"
  done; unset _p

  if [ "false" = "$network_dhcp" ]; then
    [ -z "$network_address" ] && flash_append "danger" "IP address cannot be empty." && error=1
    [ -z "$network_netmask" ] && flash_append "danger" "Networking mask cannot be empty." && error=1
    [ -z "$network_gateway" ] && flash_append "danger" "Gateway IP address cannot be empty." && error=1
    [ -z "$network_dns_1" ] && flash_append "danger" "Nameserver address cannot be empty." && error=1
    [ -z "$network_dns_2" ] && flash_append "danger" "Nameserver address cannot be empty." && error=1
  fi

  if [ -z "$error" ]; then
    :> $tmp_file
    cat /etc/network/interfaces | sed '/^auto eth0$/,/^$/d' | sed -e :a -e '/^\n*$/{$d;N;};/\n$/ba' > $tmp_file
    if [ "true" = "$network_dhcp" ]; then
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
      if [ "$network_hostname" != "$(hostname)" ]; then
        echo "$network_hostname" > /etc/hostname
        hostname "$network_hostname"
#        sed -i 's/127.0.1.1.*${hostname}/127.0.1.1\t${network_hostname}/g' /etc/hosts
        sed -i "/127.0.1.1\s/s/^.*$/127.0.1.1\t${network_hostname}/" /etc/hosts
        # FIXME: hangs on update
        killall udhcpc
        udhcpc -x hostname:$network_hostname -T 1 -t 5 -R -b -O search
      fi
    fi

    update_caminfo
    touch /tmp/network-restart.txt
    redirect_back "success" "Network settings updated."
  fi
fi
%>
<%in p/header.cgi %>

<div class="row g-4 mb-4">
  <div class="col col-md-6 col-lg-4 col-xxl-3">
    <h3>Settings</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "update" %>
      <% field_text "network_hostname" "Hostname" "Make hostname unique using MAC address information: ${network_macaddr//:/-}" %>
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
