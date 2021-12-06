#!/usr/bin/haserl
content-type: text/html

<%in _header.cgi %>
<h2>Updating settings</h2>
<%
#echo "Probe change $(printenv | grep FORM_)" | logger -t microbe-web
if [ ! -z "$FORM_hostname" ]; then
  oldhostname=$(cat /etc/hostname)
  echo "<h5>Updating hostname</h5>"
  if [ "$FORM_hostname" = "$oldhostname" ]; then
      echo "<div class=\"alert alert-warning mb-3\">"
      echo "Same hostname. Skipping."
      echo "</div>"
  else
    echo -n "<div class=\"alert alert-success mb-3 pre\">"
    echo "<b># echo ${FORM_hostname} > /etc/hostname</b>"
    echo "$(echo ${FORM_hostname} > /etc/hostname 2>&1 && echo "OK")"
    echo "<b># echo hostname ${FORM_hostname}</b>"
    echo "$(hostname ${FORM_hostname} 2>&1 && echo "OK")"
    echo "<b># sed -i 's/127.0.1.1.*${oldhostname}/127.0.1.1\t${FORM_hostname}/g' /etc/hosts</b>"
    echo "$(sed -i 's/127.0.1.1.*${oldhostname}/127.0.1.1\t${FORM_hostname}/g' /etc/hosts 2>&1 && echo "OK")"
    echo "<b># killall udhcpc</b>"
    echo "$(killall udhcpc && echo "OK")"
    echo "<b># udhcpc -x hostname:${FORM_hostname} -T 1 -t 5 -R -b -O search</b>"
    echo "$(udhcpc -x hostname:${FORM_hostname} -T 1 -t 5 -R -b -O search > /dev/null 2>&1 && echo "OK")"
    echo "</div>"
  fi
fi
if [ ! -z "$FORM_password" ]; then
  echo "<h5>Updating password</h5>"
  if [[ ! -z "$(echo "$FORM_password" | grep " ")" ]]
  then
    echo "<div class=\"alert alert-danger mb-3\">"
    echo "Password cannot have spaces!"
    echo "</div>"
  else
    echo -n "<div class=\"alert alert-secondary mb-3 pre\">"
    echo "<b># sed -i s/:admin:.*/:admin:${FORM_password}/ /etc/httpd.conf</b>"
    echo "$(sed -i s/:admin:.*/:admin:${FORM_password}/ /etc/httpd.conf 2>&1 && echo "OK")"
    echo "</div>"
  fi
fi
if [ ! -z "$FORM_ipaddr" ]; then
  echo "<h5>Updating IP address</h5>"
  if [ "$(yaml-cli -g .network.lan.ipaddr)" = "$FORM_ipaddr" ]
  then
    echo "<div class=\"alert alert-warning mb-3\">"
    echo "Same IP address. Skipping."
    echo "</div>"
  else
    echo -n "<div class=\"alert alert-success mb-3 pre\">"
    echo "<b># yaml-cli -s .network.lan.ipaddr ${FORM_ipaddr}</b>"
    echo "$(yaml-cli -s .network.lan.ipaddr ${FORM_ipaddr} 2>&1 && echo "OK")"
    echo "</div>"
  fi
fi
if [ ! -z "$FORM_netmask" ]; then
  echo "<h5>Updating IP netmask</h5>"
  if [ "$(yaml-cli -g .network.lan.netmask)" = "$FORM_netmask" ]
  then
    echo "<div class=\"alert alert-warning mb-3\">"
    echo "Same IP network mask. Skipping."
    echo "</div>"
  else
    echo -n "<div class=\"alert alert-success mb-3 pre\">"
    echo "<b># yaml-cli -s .network.lan.netmask ${FORM_netmask}</b>"
    echo "$(yaml-cli -s .network.lan.netmask ${FORM_netmask} 2>&1 && echo "OK")"
    echo "</div>"
  fi
fi
if [ ! -z "$FORM_remote" ]; then
  echo "<h5>Updating VTUNd Server</h5>"
  echo -n "<div class=\"alert alert-success mb-3 pre\">"
  if [ "$FORM_remote" = "__delete" ]; then
    echo "<b># yaml-cli -d .openvpn.vpn1.remote</b>"
    echo "$(yaml-cli -d .openvpn.vpn1.remote && echo "OK")"
  else
    echo "<b># yaml-cli -s .openvpn.vpn1.remote ${FORM_remote}</b>"
    echo "$(yaml-cli -s .openvpn.vpn1.remote ${FORM_remote} 2>&1 && echo "OK")"
  fi
  echo "</div>"
fi
%>
<div class="alert alert-danger mt-5 mb-3">
  <p>Restart needed to apply changes.</p>
  <p class="mb-0"><a href="/cgi-bin/reboot.cgi" class="btn btn-danger">Reboot the camera now</a></p>
</div>
<p><a href="/cgi-bin/network.cgi">Go back to settings</a></p>
<%in _footer.cgi %>
