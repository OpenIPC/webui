#!/bin/sh
soc_temp=$(ipcinfo --temp);
if [ -n "$soc_temp" ]; then
  soc_temp="${soc_temp}°C"
else
  soc_temp=""
fi
payload=$(printf '{"soc_temp":"%s","time_now":"%s","timezone":"%s"}' "$soc_temp" "$(date +%s)" "$(cat /etc/timezone)")
echo "HTTP/1.1 200 OK
Content-type: application/json
Pragma: no-cache
Expires: $(TZ=GMT0 date +'%a, %d %b %Y %T %Z')
Etag: \"$(cat /proc/sys/kernel/random/uuid)\"

${payload}
"
