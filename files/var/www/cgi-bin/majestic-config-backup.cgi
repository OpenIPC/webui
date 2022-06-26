#!/bin/sh
file=/etc/majestic.yaml
echo "HTTP/1.0 200 OK
Date: $(TZ=GMT0 date +'%a, %d %b %Y %T %Z')
Server: $SERVER_SOFTWARE
Content-type: text/plain
Content-Disposition: attachment; filename=majestic.yaml
Content-Length: $(ls -l $file | xargs | cut -d' ' -f5)
Cache-Control: no-store
Pragma: no-cache
"
cat $file
