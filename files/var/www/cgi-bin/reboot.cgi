#!/bin/sh
echo "HTTP/1.1 302 Moved Temporarily
Date: $(TZ=GMT0 date +'%a, %d %b %Y %T %Z')
Server: $SERVER_SOFTWARE
Content-type: text/html; charset=UTF-8
Cache-Control: no-store
Pragma: no-cache
Location: /wait.html
Status: 302 Moved Temporarily
"

sleep 5
umount -a -t nfs -l
reboot -f
