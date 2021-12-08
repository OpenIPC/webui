#!/usr/bin/haserl
<%in _common.cgi %>
<%in _header.cgi %>
<h2>Updating settings</h2>
<%
if [ ! -z "$FORM_hostname" ]; then
  oldhostname=$(cat /etc/hostname)
  if [ "$FORM_hostname" = "$oldhostname" ]; then
      report_warning "Same hostname. Skipping."
  else
    command="echo ${FORM_hostname} > /etc/hostname"
    result=$($command 2>&1)
    report_command_info "$command" "$result"

    command="hostname ${FORM_hostname}"
    result=$($command 2>&1)
    report_command_info "$command" "$result"

    command="sed -i 's/127.0.1.1.*${oldhostname}/127.0.1.1\t${FORM_hostname}/g' /etc/hosts"
    result=$($command 2>&1)
    report_command_info "$command" "$result"

    command="killall udhcpc"
    result=$($command 2>&1)
    report_command_info "$command" "$result"

    command="udhcpc -x hostname:${FORM_hostname} -T 1 -t 5 -R -b -O search"
    result=$($command 2>&1)
    report_command_info "$command" "$result"
  fi
fi

if [ ! -z "$FORM_password" ]; then
  if [[ ! -z "$(echo "$FORM_password" | grep " ")" ]]
  then
    report_error "Password cannot have spaces!"
  else
    command="sed -i s/:admin:.*/:admin:${FORM_password}/ /etc/httpd.conf"
    result=$($command 2>&1)
    report_command_info "$command" "$result"
  fi
fi

if [ ! -z "$FORM_ipaddr" ]; then
  if [ "$(yaml-cli -g .network.lan.ipaddr)" = "$FORM_ipaddr" ]
  then
    report_warning "Same IP address. Skipping."
  else
    command="yaml-cli -s .network.lan.ipaddr ${FORM_ipaddr}"
    result=$($command 2>&1)
    report_command_info "$command" "$result"
  fi
fi

if [ ! -z "$FORM_netmask" ]; then
  if [ "$(yaml-cli -g .network.lan.netmask)" = "$FORM_netmask" ]
  then
    report_warning "Same IP network mask. Skipping."
  else
    command="yaml-cli -s .network.lan.netmask ${FORM_netmask}"
    result=$($command 2>&1)
    report_command_info "$command" "$result"
  fi
fi

if [ ! -z "$FORM_remote" ]; then
  if [ "$FORM_remote" = "__delete" ]; then
    command="yaml-cli -d .openvpn.vpn1.remote"
  else
    command="yaml-cli -s .openvpn.vpn1.remote ${FORM_remote}"
  fi
  result=$($command 2>&1)
  report_command_info "$command" "$result"
fi

if [ ! -z "$FORM_timezone" ]; then
  if [ "$(cat /etc/TZ)" = "$FORM_timezone" ]
  then
    report_warning "Same timezone. Skipping."
  else
    command="echo ${FORM_timezone} > /etc/TZ"
    result=$($command 2>&1)
    report_command_info "$command" "$result"
  fi
fi
%>

<div class="alert alert-danger mt-5 mb-3">
  <p>Restart needed to apply changes.</p>
  <p class="mb-0"><a href="/cgi-bin/reboot.cgi" class="btn btn-danger">Reboot the camera now</a></p>
</div>

<p><a href="/cgi-bin/network.cgi">Go back to settings</a></p>
<%in _footer.cgi %>
