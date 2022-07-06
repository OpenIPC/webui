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
#    [ -z "$network_gateway" ] && flash_append "danger" "Gateway IP address cannot be empty." && error=1
#    [ -z "$network_dns_1" ] && flash_append "danger" "Nameserver address cannot be empty." && error=1
#    [ -z "$network_dns_2" ] && flash_append "danger" "Nameserver address cannot be empty." && error=1
  fi

  if [ -z "$error" ]; then
    :> $tmp_file
    cat /etc/network/interfaces | sed '/^auto eth0$/,/^$/d' | sed -e :a -e '/^\n*$/{$d;N;};/\n$/ba' > $tmp_file
    if [ "true" = "$network_dhcp" ]; then
      echo -e "\nauto eth0\niface eth0 inet dhcp\n  hwaddress ether \$(fw_printenv -n ethaddr || echo 00:24:B8:FF:FF:FF)" >> $tmp_file
    else
      echo -e "\nauto eth0" >> $tmp_file
      echo "iface eth0 inet static" >> $tmp_file
      echo "  hwaddress ether \$(fw_printenv -n ethaddr || echo 00:24:B8:FF:FF:FF)" >> $tmp_file
      echo "  address ${network_address}" >> $tmp_file
      echo "  netmask ${network_netmask}" >> $tmp_file

      # skip gateway if empty
      [ -n "$network_gateway" ] && echo "  gateway ${network_gateway}" >> $tmp_file

      # shift dns2 to dns1 if dns1 if empty
      if [ -z "$network_dns_1" ]; then
        network_dns_1="$network_dns_2"
        network_dns_2=""
      fi

      # set dns1 to localhost if none provided
      # [ -z "$network_dns_1" ] && network_dns_1="127.0.0.1"

      if [ -n "$network_dns_1" ]; then
        echo -n "  pre-up echo -e \"nameserver ${network_dns_1}\n" >> $tmp_file
        [ -n "$network_dns_2" ] && echo -n "nameserver ${network_dns_2}\n" >> $tmp_file
        echo "\" >/tmp/resolv.conf" >> $tmp_file
      fi

      # no need for that unless we skip rebooting
      # echo -e "nameserver ${network_dns_1}\nnameserver ${network_dns_2}" >/tmp/resolv.conf
    fi
    mv $tmp_file /etc/network/interfaces

    if [ -n "$network_hostname" ]; then
      _old_hostname="$(hostname)"
      if [ "$network_hostname" != "$_old_hostname" ]; then
        echo "$network_hostname" > /etc/hostname
        hostname "$network_hostname"
        sed -r -i "/127.0.1.1/s/(\b)${_old_hostname}(\b)/\1${network_hostname}\2/" /etc/hosts >&2
        killall udhcpc
        # page does not redirect without >/dev/null
        udhcpc -x hostname:$network_hostname -T 1 -t 5 -R -b -O search > /dev/null
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
  <div class="col col-md-6 col-lg-4 mb-4">
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
  <div class="col col-md-6 col-lg-8">
    <% ex "cat /etc/hostname" %>
    <% ex "cat /etc/hosts" %>
    <% ex "cat /etc/network/interfaces" %>
    <% ex "ip address" %>
    <% ex "ip route list" %>
    <% [ -f /etc/resolv.conf ] && ex "cat /etc/resolv.conf" %>
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
