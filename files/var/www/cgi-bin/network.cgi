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
  source $tmp_file

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
%>

<%in p/header.cgi %>

<% if [ -f /tmp/network-restart.txt ]; then %>
  <div class="alert alert-danger">
    <h4>Network settings have been updated.</h4>
    <p>Restart needed to apply changes.</p>
    <% button_reboot %>
  </div>
<% fi %>

<div class="row">
  <div class="col col-md-6 col-lg-4 col-xxl-3">
    <h3>Settings</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <input type="hidden" name="action" value="update">

      <p class="string">
        <label for="network_hostname" class="form-label">Hostname</label>
        <input type="text" id="network_hostname" name="network_hostname" class="form-control data-pattern=host" value="<%= $hostname %>">
        <span class="hint text-secondary">Make hostname unique using MAC address information: <%= $macaddr %></span>
      </p>
      <p class="boolean">
        <span class="form-check form-switch">
        <input type="hidden" name="network_dhcp" id="network_dhcp-false" value="false">
        <input type="checkbox" id="network_dhcp" name="network_dhcp" value="true" class="form-check-input" role="switch"<% [ "true" = "$dhcp" ] && echo " checked" %>>
        <label for="network_dhcp" class="form-label form-check-label">Use DHCP</label>
        </span>
      </p>
      <p class="string">
        <label for="network_address" class="form-label">IP Address</label>
        <input type="text" id="network_address" name="network_address" class="form-control" value="<%= $ipaddr %>">
      </p>
      <p class="string">
        <label for="network_netmask" class="form-label">IP Netmask</label>
        <input type="text" id="network_netmask" name="network_netmask" class="form-control" value="<%= $netmask %>">
      </p>
      <p class="string">
        <label for="network_gateway" class="form-label">Gateway</label>
        <input type="text" id="network_gateway" name="network_gateway" class="form-control" value="<%= $gateway %>">
      </p>
      <p class="string">
        <label for="network_dns_1" class="form-label">DNS 1</label>
        <input type="text" id="network_dns_1" name="network_dns_1" class="form-control" value="<%= $dns_1 %>">
      </p>
      <p class="string">
        <label for="network_dns_2" class="form-label">DNS 2</label>
        <input type="text" id="network_dns_2" name="network_dns_2" class="form-control" value="<%= $dns_2 %>">
      </p>
      <p class="button submit mt-2"><input type="submit" class="btn btn-primary" value="Save changes"></p>
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
