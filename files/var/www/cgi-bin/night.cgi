#!/bin/sh
echo "HTTP/1.1 200 OK
Date: $(TZ=GMT0 date +'%a, %d %b %Y %T %Z')
Server: $SERVER_SOFTWARE
Content-type: text/plain; charset=UTF-8
Cache-Control: no-store
Pragma: no-cache
"

# parse parameters from query string
eval $(echo ${QUERY_STRING//&/;})

case "$mode" in
  on)
    curl http://admin:@127.0.0.1/night/on
    ;;
  off)
    curl http://admin:@127.0.0.1/night/off
    ;;
  toggle)
    curl http://admin:@127.0.0.1/night/toggle
    ;;
  *)
    ;;
esac
