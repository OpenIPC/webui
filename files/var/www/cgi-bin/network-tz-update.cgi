#!/usr/bin/haserl
<%in _common.cgi %>
<%in _header.cgi %>
<%
if [ -z "$FORM_tz_data" ]; then
  error="Empty timezone value. Skipping."
elif [ "$(cat /etc/TZ)" = "$FORM_tz_data" ]; then
  error="Same timezone. Skipping."
fi

if [ ! -z "$error"]; then
  report_error "$output"
else
  command="echo \"$FORM_tz_data\" > /etc/TZ && export TZ=\"$FORM_tz_data\""
  output=$(echo "${FORM_tz_data}" > /etc/TZ && export TZ="${FORM_tz_data}" 2>&1)
  result=$?
  if [ "0" -eq "$result" ]; then
    report_command_success "$command" "$output"
  else
    report_command_error "$command" "$output"
  fi
  echo "<a class=\"btn btn-primary\" href=\"/cgi-bin/network-ntp.cgi\">Go to NTP settings</a>"
fi
%>
<%in _footer.cgi %>
