#!/bin/sh

# read IRCUT pins from bootloader environment
PIN=$(fw_printenv -n irled_pin)

# read IRCUT pins from majestic config, if empty
[ -z "$PIN" ] && PIN=$(cli -g .nightMode.backlightPin)

if [ -z "$PIN" ]; then
	echo "Please define IR LED pin"
	echo "fw_setenv irled_pin1 <pin>"
	exit 1
fi

# parse parameters from query string
eval $(echo ${QUERY_STRING//&/;})

# set parameters from cli, if empty
[ -z "$mode" ] && mode=$1

case "$mode" in
"on")
	gpio set $PIN
	;;
"off")
	gpio clear $PIN
	;;
*)
	;;
esac

echo "HTTP/1.1 200 OK
Content-type: application/json
Pragma: no-cache
Expires: $(TZ=GMT0 date +'%a, %d %b %Y %T %Z')
Etag: \"$(cat /proc/sys/kernel/random/uuid)\"

{\"irled\":\"${mode}\"}
"
