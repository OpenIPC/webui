#!/bin/sh

# parse parameters from query string
[ -n "$QUERY_STRING" ] && eval $(echo "$QUERY_STRING" | sed "s/&/;/g")

# quit if no mode set
if [ -z "$mode" ]; then
	echo "HTTP/1.1 400 Bad Request"
	echo # separate headers from content
	echo "missing required mode parameter"
	exit 1
fi

# use ir850 as default LED if not set
[ -z "$type" ] && type="ir850"

case "$mode" in
	off | on | toggle)
		/usr/sbin/irled.sh "$mode" "$type"
		echo "HTTP/1.1 200 OK
Content-type: application/json
Pragma: no-cache
Expires: $(TZ=GMT0 date +'%a, %d %b %Y %T %Z')
Etag: \"$(cat /proc/sys/kernel/random/uuid)\"

{\"led_${type}\":\"${mode}\"}
"
		;;
	*)
		echo "HTTP/1.1 400 Bad Request"
		echo # separate headers from content
		echo "unknown mode"
		exit 1
		;;
esac

exit 0