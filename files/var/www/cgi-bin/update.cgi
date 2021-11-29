#!/usr/bin/haserl
content-type: text/html

<%
action=$FORM_action
iface=$FORM_iface
#project=$(uci get microbe.webadmin.project)
#sense=$FORM_sense

h1_ttu() { echo "<h1>Trying to update...</h1>"; }
h1_ttr() { echo "<h1>Trying to reboot. Please wait...</h1>"; }
gohome() { echo "<script>//setTimeout('window.location=\"/cgi-bin/index.cgi\"', $1);</script>"; }
%>
<%in _header.cgi %>

<%
  echo "Probe change $(printenv | grep FORM_)" | logger -t microbe-web

  case $action in
    reboot)
      h1_ttr
      gohome 30000;
      reboot
      ;;
    trace)
      echo "<nav><a href=\"/cgi-bin/monitor.cgi\">Monitor Tool</a></nav>"
      echo "<h2>Trace Route</h2>"
      echo "<pre>"
      if [ ${iface} = "auto" ]; then
        traceroute ${sense}
      else
        traceroute -i ${iface} ${sense}
      fi
      echo "</pre>"
      ;;
    update)
      echo "<h2>Updating settings</h2>"
      if [ ! -z "$FORM_hostname" ]; then
        oldhostname=$(cat /etc/hostname)
        newhostname=$FORM_hostname
        echo "<h3>Updating hostname</h3>"
        echo "<pre>"
        if [ "$newhostname" = "$oldhostname" ]; then
          echo "Same hostname. Skipping."
        else
  #        ${newhostname} > /tmp/etc/hostname 2>&1
          echo $(hostname $newhostname 2>&1 || true)
          echo $(sed -i "s/127.0.1.1.*${oldhostname}/127.0.1.1\t${newhostname}/g" /tmp/etc/hosts 2>&1 || true)
        fi
        echo "</pre>"
      fi
      if [ ! -z "$FORM_password" ]; then
        echo "<h3>Updating password</h3>"
        echo "<pre>"
        echo $(sed -i "s/:admin:.*/:admin:${FORM_password}/g" /etc/httpd.conf 2>&1 || true)
        echo "</pre>"
      fi
      if [ ! -z "$FORM_ipaddr" ]; then
        echo "<h3>Updating IP address</h3>"
        echo "<pre>"
        echo $(uci set network.lan.ipaddr=${FORM_ipaddr} 2>&1 && uci commit network 2>&1 || true)
        echo "</pre>"
    fi
      if [ ! -z "$FORM_netmask" ]; then
        echo "<h3>Updating IP netmask</h3>"
        echo "<pre>"
        echo $(uci set network.lan.netmask=${FORM_netmask} 2>&1 && uci commit network 2>&1 || true)
        echo "</pre>"
    fi
      if [ ! -z "$FORM_remote" ]; then
        echo "<h3>Updating VTUNd Server</h3>"
        echo "<pre>"
        echo $(uci set openvpn.vpn1.remote=${FORM_remote} 2>&1 && uci commit openvpn 2>&1 || true)
        echo "</pre>"
      fi
      gohome 3000;
      ;;
    ping)
      echo "<nav><a href=\"/cgi-bin/monitor.cgi\">Monitor Tool</a></nav>"
      echo "<h3>Ping Quality</h3>"
      echo "<pre>"
      if [ ${iface} = "auto" ]; then
        ping -c 15 -s 1500 ${sense}
      else
        ping -c 15 -s 1500 -I ${iface} ${sense}
      fi
      echo "</pre>"
      ;;
    *)
      echo "Unknown action!";
      ;;
  esac
%>
<%in _footer.cgi %>
