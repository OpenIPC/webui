#!/usr/bin/haserl
<%in p/common.cgi %>
<%
:> /tmp/ntp.conf
for i in $(printenv|grep POST_|sort 2>&1); do
  s=$(echo $i | cut -d= -f2)
  [ -n "$s" ] && echo "server ${s} iburst" >> /tmp/ntp.conf
done
mv /tmp/ntp.conf /etc/ntp.conf
flash_save "success" "$t_ntp_9"
redirect_to "/cgi-bin/network-ntp.cgi"
%>
