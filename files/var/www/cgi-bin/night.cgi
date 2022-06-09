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
echo -e "HTTP/1.1 200 OK\nDate: $(TZ=GMT date +\"%a, %d %b %Y %T %Z\")\nContent-Type: text/plain; charset=utf-8\nServer: httpd\n\n200 OK"
%>
