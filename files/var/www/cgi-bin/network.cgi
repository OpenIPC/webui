#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="network"
page_title="Network settings"
params="address dhcp dns_1 dns_2 gateway hostname netmask interface wifi_device wifi_ssid wifi_password"
tmp_file=/tmp/${plugin}.conf

profiles="$(grep -r '$1..=' /etc/wireless | cut -d '"' -f 4 | sort | grep -e ${soc} -e generic)"
wlandev="$(fw_printenv -n wlandev)"
wlanssid="$(fw_printenv -n wlanssid)"
wlanpass="$(fw_printenv -n wlanpass)"

if [ "POST" = "$REQUEST_METHOD" ]; then
	case "$POST_action" in
		changemac)
			if echo "$POST_mac_address" | grep -Eiq '^([0-9a-f]{2}[:-]){5}([0-9a-f]{2})$'; then
				fw_setenv ethaddr $POST_mac_address
				update_caminfo
				redirect_to "reboot.cgi"
			else
				redirect_back "warning" "${POST_mac_address} is as invalid MAC address."
			fi
			;;
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

			[ -z "$network_interface" ] && flash_append "danger" "Default network interface cannot be empty." && error=1

			if [ "false" = "$network_dhcp" ]; then
				network_mode="static"
				[ -z "$network_address" ] && flash_append "danger" "IP address cannot be empty." && error=1
				[ -z "$network_netmask" ] && flash_append "danger" "Networking mask cannot be empty." && error=1
			else
				network_mode="dhcp"
			fi

			if [ "wlan0" = "$network_interface" ]; then
				[ -z "$network_wifi_device" ] && flash_append "danger" "WLAN Device cannot be empty." && error=1
				[ -z "$network_wifi_ssid" ] && flash_append "danger" "WLAN SSID cannot be empty." && error=1
				[ -z "$network_wifi_password" ] && flash_append "danger" "WLAN Password cannot be empty." && error=1
			fi

			if [ -z "$error" ]; then
				command="setnetiface.sh"
				command="${command} -i $network_interface"
				command="${command} -m $network_mode"
				command="${command} -h $network_hostname"

				if [ "wlan0" = "$network_interface" ]; then
					command="${command} -r $network_wifi_device"
					command="${command} -s $network_wifi_ssid"
					command="${command} -p $network_wifi_password"
				fi

				if [ "dhcp" != "$network_mode" ]; then
					command="${command} -a $network_address"
					command="${command} -n $network_netmask"
					[ -n "$network_gateway" ] && command="${command} -g $network_gateway"
					[ -n "$network_dns_1" ] && command="${command} -d $network_dns_1"
					[ -n "$network_dns_2" ] && command="${command},${network_dns_2}"
				fi

				echo "$command" >>/tmp/webui.log
				eval "$command" >/dev/null 2>&1

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
      <% field_text "network_hostname" "Hostname" %>
      <% field_select "network_interface" "Network interface" "eth0 wlan0" %>
      <% field_select "network_wifi_device" "WLAN Device" "$profiles" %>
      <% field_text "network_wifi_ssid" "WLAN SSID" "" "$wlanssid" %>
      <% field_text "network_wifi_password" "WLAN Password" "" "$wlanpass" %>

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
    const ids = ['network_wifi_device','network_wifi_ssid','network_wifi_password'];
    if ($('#network_interface').value == 'wlan0') {
      ids.forEach(id => $('#' + id + '_wrap').classList.remove('d-none'));
    } else {
      ids.forEach(id => $('#' + id + '_wrap').classList.add('d-none'));
    }
  }

  $('#network_interface').addEventListener('change', toggleIface);
  $('#network_dhcp[type=checkbox]').addEventListener('change', toggleDhcp);
  $('#network_wifi_device').value = "<%= $wlandev %>";

  toggleIface();
  toggleDhcp();
</script>

<%in p/footer.cgi %>
