#!/usr/bin/haserl
<%in p/common.cgi %>
<%
if [ -z "$POST_tz_name" ]; then
  flash_save "warning" "$t_tz_1"
elif [ -z "$POST_tz_data" ]; then
  flash_save "warning" "$t_tz_2"
else
  [ "$tz_data" != "$POST_tz_data" ] && echo "${POST_tz_data}" > /etc/TZ
  [ "$tz_name" != "$POST_tz_name" ] && echo "${POST_tz_name}" > /etc/tz_name
  flash_save "success" "$t_tz_3"
  update_caminfo
fi
redirect_to "/cgi-bin/network-ntp.cgi"
%>
