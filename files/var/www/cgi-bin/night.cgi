#!/usr/bin/haserl
<%
case "$POST_mode" in
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
echo "HTTP/1.1 200 OK
Date: $(TZ=GMT date +"%a, %d %b %Y %T %Z")
Content-Type: text/plain; charset=utf-8
Server: httpd

200 OK
"
%>
