#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="network"
page_title="Network settings"
params="address dhcp dns_1 dns_2 gateway hostname netmask wifi_modules wifi_ssid wifi_password"
tmp_file=/tmp/${plugin}.conf

if [ "POST" = "$REQUEST_METHOD" ]; then
  case "$POST_action" in
    reset)
      /usr/sbin/sysreset.sh -n
      redirect_back
      ;;
    update)
      # parse values from parameters
      for _p in $params; do
        eval ${plugin}_${_p}=\$POST_${plugin}_${_p}
        sanitize "${plugin}_${_p}"
      done; unset _p

      if [ "false" = "$network_dhcp" ]; then
        network_mode="static"
        [ -z "$network_default_interface" ] && flash_append "danger" "Default network interface cannot be empty." && error=1
        [ -z "$network_address" ] && flash_append "danger" "IP address cannot be empty." && error=1
        [ -z "$network_netmask" ] && flash_append "danger" "Networking mask cannot be empty." && error=1
    #    [ -z "$network_gateway" ] && flash_append "danger" "Gateway IP address cannot be empty." && error=1
    #    [ -z "$network_dns_1" ] && flash_append "danger" "Nameserver address cannot be empty." && error=1
    #    [ -z "$network_dns_2" ] && flash_append "danger" "Nameserver address cannot be empty." && error=1
      else
        network_mode="dhcp"
      fi

      if [ -z "$error" ]; then
        command="setnetiface.sh"
        command="${command} -i $network_default_interface"
        command="${command} -m $network_mode"
        command="${command} -n $network_hostname"

        if [ "wlan0" = "$network_default_interface" ]; then
          command="${command} -s $network_wifi_ssid"
          command="${command} -p $network_wifi_password"
          command="${command} -k $network_wifi_modules"
          command="${command} -t wifi"
        fi

        if [ "dhcp" != "$network_mode" ]; then
          command="${command} -a $network_address"
          command="${command} -n $network_netmask"
          command="${command} -g $network_gateway"
          command="${command} -d $network_dns_1"
          command="${command} -D $network_dns_2"
        fi

        echo "$command" >>/tmp/webui.log
        eval "$command" >/dev/null 2>&1

        /etc/init.d/S40network restart >/dev/null
        update_caminfo
        redirect_back "success" "Network settings updated."
      fi
      ;;
  esac
fi
%>
<%in p/header.cgi %>

<div class="row g-4">
  <div class="col col-md-6 col-lg-4 mb-4">
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "update" %>
      <% field_text "network_hostname" "Hostname" "Make hostname unique using MAC address information: ${network_macaddr//:/-}" %>
      <% field_select "network_default_interface" "Default network interface" "$network_interfaces" %>
      <% field_text "network_wifi_modules" "WiFi modules" %>
      <% field_text "network_wifi_ssid" "WiFi SSID" %>
      <% field_text "network_wifi_password" "WiFi Password" %>

      <% field_switch "network_dhcp" "Use DHCP" %>
      <% field_text "network_address" "IP Address" %>
      <% field_text "network_netmask" "IP Netmask" %>
      <% field_text "network_gateway" "Gateway" %>
      <% field_text "network_dns_1" "DNS 1" %>
      <% field_text "network_dns_2" "DNS 2" %>
      <% button_submit %>
    </form>

    <div class="alert alert-danger mt-4">
      <h5>Reset network configuration</h5>
      <p>Restore the config file bundled with firmware. All changes to the default configuration will be lost!</p>
      <form action="<%= $SCRIPT_NAME %>" method="post" enctype="multipart/form-data">
        <% field_hidden "action" "reset" %>
        <% button_submit "Reset config" "danger" %>
      </form>
    </div>
  </div>
  <div class="col col-md-6 col-lg-8">
    <% ex "cat /etc/hostname" %>
    <% ex "cat /etc/hosts" %>
    <% ex "cat /etc/network/interfaces" %>
  <% for i in $(ls -1 /etc/network/interfaces.d/); do %>
    <% ls /sys/class/net | grep -q $i && ex "cat /etc/network/interfaces.d/$i" %>
  <% done %>
    <% ex "ip address" %>
    <% ex "ip route list" %>
    <% [ -f /etc/resolv.conf ] && ex "cat /etc/resolv.conf" %>
  </div>
</div>

<script>
  function toggleDhcp() {
    const c = $('#network_dhcp[type=checkbox]').checked;
    const ids = ['network_address','network_netmask','network_gateway','network_dns_1','network_dns_2'];
    ids.forEach(id => {
      $('#' + id).disabled = c;
      let el = $('#' + id + '_wrap');
      c ? el.classList.add('d-none') : el.classList.remove('d-none');
    });
  }

  function toggleIface() {
    const ids = ['network_wifi_modules','network_wifi_ssid','network_wifi_password'];
    if ($('#network_default_interface').value == 'wlan0') {
      ids.forEach(id => $('#' + id + '_wrap').classList.remove('d-none'));
    } else {
      ids.forEach(id => $('#' + id + '_wrap').classList.add('d-none'));
    }
  }

  $('#network_default_interface').addEventListener('change', toggleIface);
  $('#network_dhcp[type=checkbox]').addEventListener('change', toggleDhcp);

  toggleIface();
  toggleDhcp();
</script>

<%in p/footer.cgi %>
