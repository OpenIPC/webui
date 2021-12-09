#!/usr/bin/haserl
<%in _common.cgi %>
<%
truncate -s 0 /etc/ntp.conf
for i in $(printenv | grep POST_ | sort 2>&1); do
  s=$(echo $i | cut -d= -f2);
  [ ! -z "$s" ] && echo "server $s iburst" >> /etc/ntp.conf 2>&1
done
#mv /tmp/ntp.conf /etc/ntp.conf 2>&1
redirect_to "/cgi-bin/network-ntp.cgi"
%>
