#!/bin/sh

# parse parameters from query string
[ -n "$QUERY_STRING" ] && eval $(echo "$QUERY_STRING" | sed "s/&/;/g")

# quit if no mode set
if [ -z "$mode" ]; then
	echo "HTTP/1.1 400 Bad Request"
	echo # separate headers from content
	echo "missing required pin1 parameter"
	exit 1
fi

case "$mode" in
	off | on | toggle)
		/usr/sbin/ircut.sh "$mode" $pin1 $pin2
		echo "HTTP/1.1 200 OK
Content-type: application/json
Pragma: no-cache
Expires: $(TZ=GMT0 date +'%a, %d %b %Y %T %Z')
Etag: \"$(cat /proc/sys/kernel/random/uuid)\"

{\"ircut\":\"${mode}\"}
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