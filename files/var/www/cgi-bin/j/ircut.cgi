#!/bin/sh

# read IRCUT pins from bootloader environment
PIN1=$(fw_printenv -n ircut_pin1)
PIN2=$(fw_printenv -n ircut_pin2)

# read IRCUT pins from majestic config, if empty
[ -z "$PIN1" ] && PIN1=$(cli -g .nightMode.irCutPin1)
[ -z "$PIN2" ] && PIN2=$(cli -g .nightMode.irCutPin2)

if [ -z "$PIN1" ]; then
	echo "Please define IR-CUT pin"
	echo "fw_setenv ircut_pin1 <pin>"
	exit 1
fi

if [ -z "$PIN2" ]; then
	echo "Unless you have a single GPIO IR-Cut driver, please define the second pin:"
	echo "fw_setenv ircut_pin2 <pin>"
fi

# parse parameters from query string
eval $(echo ${QUERY_STRING//&/;})

# set parameters from cli, if empty
[ -z "mode" ] && mode=$1

case "$mode" in
"on")
	if [ -z "$PIN2" ]; then
		gpio set $PIN1
	else
		gpio set $PIN1
		gpio clear $PIN2
		usleep 10000
		gpio clear $PIN1
		gpio clear $PIN2
	fi
	;;
"off")
	if [ -z "$PIN2" ]; then
		gpio clear $PIN1
	else
		gpio clear $PIN1
		gpio set $PIN2
		usleep 10000
		gpio clear $PIN1
		gpio clear $PIN2
	fi
	;;
*)
	;;
esac

echo "HTTP/1.1 200 OK
Content-type: application/json
Pragma: no-cache
Expires: $(TZ=GMT0 date +'%a, %d %b %Y %T %Z')
Etag: \"$(cat /proc/sys/kernel/random/uuid)\"

{\"ircut\":\"${mode}\"}
"
