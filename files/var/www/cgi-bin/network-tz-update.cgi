#!/usr/bin/haserl
<%in _common.cgi %>
<%
if [ -z "$POST_tz_name" ]; then
  flash_save "warning" "$tMsgEmptyTimezoneName"
elif [ -z "$POST_tz_data" ]; then
  flash_save "warning" "$tMsgEmptyTimezoneValue"
elif [ "$(cat /etc/TZ)" = "$POST_tz_data" ]; then
  flash_save "warning" "$tMsgSameTimezone"
else
  echo "${POST_tz_data}" > /etc/TZ
  echo "${POST_tz_name}" > /etc/tzname
  flash_save "success" "$tMsgTimezoneUpdated"
fi
redirect_to "/cgi-bin/network-ntp.cgi"
%>
