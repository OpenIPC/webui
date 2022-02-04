#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleNetworkUpdate"

if [ -z "$POST_dhcp" ]; then
  [ -z "$POST_ipaddr" ] && error="IP address cannot be empty."
  [ -z "$POST_netmask" ] && error="Networking mask cannot be empty."
  [ -z "$POST_gateway" ] && error="Gateway IP address cannot be empty."
fi

if [ -n "$error" ]; then
  flash_save "danger" "$error"
  redirect_to "/cgi-bin/network.cgi"
fi

tmp_file=/tmp/interfaces
z="    "
%>
<%
if [ -n "$POST_hostname" ]; then
  oldhostname=$(cat /etc/hostname)
  if [ "$POST_hostname" != "$oldhostname" ]; then
    echo ${POST_hostname} > /etc/hostname
    hostname ${POST_hostname}
    sed -i 's/127.0.1.1.*${oldhostname}/127.0.1.1\t${POST_hostname}/g' /etc/hosts
    killall udhcpc
    udhcpc -x hostname:${POST_hostname} -T 1 -t 5 -R -b -O search
  fi
fi

cat /etc/network/interfaces > ${tmp_file}
sed -i '/^auto eth0$/,/^$/d' ${tmp_file}
echo -e "\nauto eth0" >> ${tmp_file}
if [ ! -z "$POST_dhcp" ]; then
  echo -e "iface eth0 inet dhcp\n" >> ${tmp_file}
else
  echo -e "iface eth0 inet static\n${z}address ${POST_ipaddr}\n${z}netmask ${POST_netmask}\n${z}gateway ${POST_gateway}\n" >> ${tmp_file}
fi
mv ${tmp_file} /etc/network/interfaces
%>
<%in _header.cgi %>
<div class="alert alert-danger mt-5 mb-3">
  <p><%= $tMsgRestatNeeded %></p>
  <p class="mb-0"><a href="/cgi-bin/reboot.cgi" class="btn btn-danger"><%= $tButtonReboot %></a></p>
</div>
<p><a href="/cgi-bin/network.cgi"><%= $tButtonGoBackToSettings %></a></p>
<%in _footer.cgi %>
