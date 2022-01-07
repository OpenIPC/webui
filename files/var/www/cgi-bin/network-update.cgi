#!/usr/bin/haserl
<% page_title="Updating settings" %>
<%in _common.cgi %>
<%in _header.cgi %>
<%
if [ ! -z "$POST_hostname" ]; then
  oldhostname=$(cat /etc/hostname)
  if [ "$POST_hostname" = "$oldhostname" ]; then
    report_warning "Same hostname. Skipping."
  else
    command="echo ${POST_hostname} > /etc/hostname"
    result=$(echo ${POST_hostname} > /etc/hostname 2>&1)
    report_command_info "$command" "$result"

    command="hostname ${POST_hostname}"
    result=$(hostname ${POST_hostname} 2>&1)
    report_command_info "$command" "$result"

    command="sed -i 's/127.0.1.1.*${oldhostname}/127.0.1.1\t${POST_hostname}/g' /etc/hosts"
    result=$(sed -i 's/127.0.1.1.*${oldhostname}/127.0.1.1\t${POST_hostname}/g' /etc/hosts 2>&1)
    report_command_info "$command" "$result"

    command="killall udhcpc"
    result=$(killall udhcpc 2>&1)
    report_command_info "$command" "$result"

    command="udhcpc -x hostname:${POST_hostname} -T 1 -t 5 -R -b -O search"
    result=$(udhcpc -x hostname:${POST_hostname} -T 1 -t 5 -R -b -O search 2>&1)
    report_command_info "$command" "$result"
  fi
fi

if [ ! -z "$POST_ipaddr" ]; then
  if [ "$(yaml-cli -g .network.lan.ipaddr)" = "$POST_ipaddr" ]; then
    report_warning "Same IP address. Skipping."
  else
    command="yaml-cli -s .network.lan.ipaddr ${POST_ipaddr}"
    result=$(yaml-cli -s .network.lan.ipaddr ${POST_ipaddr} 2>&1)
    report_command_info "$command" "$result"
  fi
fi

if [ ! -z "$POST_netmask" ]; then
  if [ "$(yaml-cli -g .network.lan.netmask)" = "$POST_netmask" ]; then
    report_warning "Same IP network mask. Skipping."
  else
    command="yaml-cli -s .network.lan.netmask ${POST_netmask}"
    result=$(yaml-cli -s .network.lan.netmask ${POST_netmask} 2>&1)
    report_command_info "$command" "$result"
  fi
fi

if [ ! -z "$POST_remote" ]; then
  if [ "$POST_remote" = "__delete" ]; then
    command="yaml-cli -d .openvpn.vpn1.remote"
    result=$(yaml-cli -d .openvpn.vpn1.remote 2>&1)
  else
    command="yaml-cli -s .openvpn.vpn1.remote ${POST_remote}"
    result=$(yaml-cli -s .openvpn.vpn1.remote ${POST_remote} 2>&1)
  fi
  report_command_info "$command" "$result"
fi
%>
<div class="alert alert-danger mt-5 mb-3">
  <p>Restart needed to apply changes.</p>
  <p class="mb-0"><a href="/cgi-bin/reboot.cgi" class="btn btn-danger">Reboot the camera now</a></p>
</div>
<p><a href="/cgi-bin/network.cgi">Go back to settings</a></p>
<%in _footer.cgi %>
