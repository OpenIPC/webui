#!/bin/sh
diff /rom/etc/majestic.yaml /etc/majestic.yaml > /tmp/majestic.patch
echo "HTTP/1.0 200 OK
Date: $(TZ=GMT0 date +'%a, %d %b %Y %T %Z')
Server: $SERVER_SOFTWARE
Content-type: text/plain
Content-Disposition: attachment; filename=majestic.$(date +"%s").patch
Content-Length: $(ls -l /tmp/majestic.patch | xargs | cut -d' ' -f5)
Cache-Control: no-store
Pragma: no-cache
"
cat /tmp/majestic.patch
