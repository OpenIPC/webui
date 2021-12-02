#!/usr/bin/haserl
content-type: text/html

<%
#project=$(uci get microbe.webadmin.project)
gohome() {
  echo "<script>"
  echo "//setTimeout('window.location=\"/\"', $1);"
  echo "</script>"
}
%>
<%in _header.cgi %>
<%
  echo "Probe change $(printenv | grep FORM_)" | logger -t microbe-web

  case $FORM_action in
    ping)
      echo "<h3>Ping Quality</h3>"
      echo "<pre>"
      if [ "$FORM_iface" = "auto" ]; then
        echo "# ping -c 15 -s 1500 ${FORM_target}"
        echo "$(ping -c 15 -s 1500 ${FORM_target} 2>&1)"
      else
        echo "# ping -c 15 -s 1500 -I ${FORM_iface} ${FORM_target}"
        echo "$(ping -c 15 -s 1500 -I ${FORM_iface} ${FORM_target} 2>&1)"
      fi
      echo "</pre>"
      ;;
    reboot)
      echo "<h1>Trying to reboot. Please wait...</h1>"
      gohome 30000;
      reboot
      ;;
    reset)
      echo "<h2>Resetting Majestic configuration<h2>"
      echo "# cp /rom/etc/majestic.yaml /etc/majestic.yaml"
      echo "$(cp /rom/etc/majestic.yaml /etc/majestic.yaml 2>&1)"
      gohome 3000;
      ;;
    trace)
      echo "<h2>Trace Route</h2>"
      echo "<pre>"
      if [ "$FORM_iface" = "auto" ]; then
        echo "# traceroute $FORM_target"
        echo "$(traceroute $FORM_target 2>&1)"
      else
        echo "# traceroute -i $FORM_iface $FORM_target"
        echo "$(traceroute -i $FORM_iface $FORM_target 2>&1)"
      fi
      echo "</pre>"
      ;;
    update)
      echo "<h2>Updating settings</h2>"
      if [ ! -z "$FORM_hostname" ]; then
        oldhostname=$(cat /etc/hostname)
        echo "<h3>Updating hostname</h3>"
        echo "<pre>"
        if [ "$FORM_hostname" = "$oldhostname" ]; then
          echo "Same hostname. Skipping."
        else
          echo "# echo \"${FORM_hostname}\" > /etc/hostname"
          echo "$(echo \"${FORM_hostname}\" > /etc/hostname 2>&1)"

          echo "# sed -i 's/127.0.1.1.*${oldhostname}/127.0.1.1\t${FORM_hostname}/g' /etc/hosts"
          echo "$(sed -i 's/127.0.1.1.*${oldhostname}/127.0.1.1\t${FORM_hostname}/g' /etc/hosts 2>&1)"
        fi
        echo "</pre>"
      fi
      if [ ! -z "$FORM_password" ]; then
        echo "<h3>Updating password</h3>"
        echo "<pre>"
        if [[ ! -z "$(echo "$FORM_password" | grep " ")" ]]
	then
	  echo "Password cannot have a space!"
	else
          echo "# sed -i s/:admin:.*/:admin:${FORM_password}/ /etc/httpd.conf"
          echo "$(sed -i s/:admin:.*/:admin:${FORM_password}/ /etc/httpd.conf 2>&1)"
	fi
        echo "</pre>"
      fi
      if [ ! -z "$FORM_ipaddr" ]; then
        echo "<h3>Updating IP address</h3>"
        echo "<pre>"
        echo "# yaml-cli -s .network.lan.ipaddr ${FORM_ipaddr}"
        echo "$(yaml-cli -s .network.lan.ipaddr ${FORM_ipaddr} 2>&1)"
        echo "</pre>"
    fi
      if [ ! -z "$FORM_netmask" ]; then
        echo "<h3>Updating IP netmask</h3>"
        echo "<pre>"
        echo "# yaml-cli -s .network.lan.netmask ${FORM_netmask}"
        echo "$(yaml-cli -s .network.lan.netmask ${FORM_netmask} 2>&1)"
        echo "</pre>"
    fi
      if [ ! -z "$FORM_remote" ]; then
        echo "<h3>Updating VTUNd Server</h3>"
        echo "<pre>"
	if [ "$FORM_remote" = "__delete" ]; then
          echo "# yaml-cli -d .openvpn.vpn1.remote"
          echo "$(yaml-cli -d .openvpn.vpn1.remote)"
	else
          echo "# yaml-cli -s .openvpn.vpn1.remote ${FORM_remote}"
          echo "$(yaml-cli -s .openvpn.vpn1.remote ${FORM_remote} 2>&1)"
        fi
        echo "</pre>"
      fi
      gohome 3000;
      ;;
    *)
      echo "Unknown action \"${FORM_action}\".";
      ;;
  esac
%>
<h4>All changes will be applied on reboot!</h4>
<%in _footer.cgi %>
