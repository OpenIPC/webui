#!/usr/bin/haserl
<%in _common.cgi %>
<%
if [ -z "$POST_tz_name" ]; then
  flash_save "warning" "Empty timezone name. Skipping."
elif [ -z "$POST_tz_data" ]; then
  flash_save "warning" "Empty timezone value. Skipping."
elif [ "$(cat /etc/TZ)" = "$POST_tz_data" ]; then
  flash_save "warning" "Same timezone. Skipping."
else
  echo "${POST_tz_data}" > /etc/TZ
  echo "${POST_tz_name}" > /etc/tzname
  flash_save "success" "Timezone updated."
fi
redirect_to "/cgi-bin/network-ntp.cgi"
%>