#!/usr/bin/haserl
<%in _common.cgi %>
<%
truncate -s 0 /tmp/ntp.conf
for i in $(printenv | grep POST_ | sort 2>&1); do
  s=$(echo $i | cut -d= -f2);
  [ ! -z "$s" ] && echo "server $s iburst" >> /tmp/ntp.conf
done
mv /tmp/ntp.conf /etc/ntp.conf
flash_save "success" "NTP servers updated."
redirect_to "/cgi-bin/network-ntp.cgi"
%>
