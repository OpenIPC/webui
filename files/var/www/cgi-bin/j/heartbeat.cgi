#!/bin/sh
soc_temp=$(ipcinfo --temp 2>/dev/null)
if [ -n "$soc_temp" ]; then
	soc_temp="${soc_temp}°C"
else
	soc_temp=""
fi
mem_total=$(awk '/MemTotal/ {print $2}' /proc/meminfo)
mem_free=$(awk '/MemFree/ {print $2}' /proc/meminfo)
mem_used=$(( 100-($mem_free/($mem_total/100)) ))
overlay_used=$(df | grep /overlay | xargs | cut -d' ' -f5)
payload=$(printf '{"soc_temp":"%s","time_now":"%s","timezone":"%s","mem_used":"%d","overlay_used":"%d"}' "$soc_temp" "$(date +%s)" "$(cat /etc/timezone)" "$mem_used" "${overlay_used//%/}")
echo "HTTP/1.1 200 OK
Content-type: application/json
Pragma: no-cache
Expires: $(TZ=GMT0 date +'%a, %d %b %Y %T %Z')
Etag: \"$(cat /proc/sys/kernel/random/uuid)\"

${payload}
"
