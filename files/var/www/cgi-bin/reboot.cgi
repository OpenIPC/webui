#!/usr/bin/haserl
<%in p/common.cgi %>
<%
touch /tmp/webjob.lock
  echo "HTTP/1.1 302 Moved Temporarily
Content-type: text/html; charset=UTF-8
Cache-Control: no-store
Pragma: no-cache
Date: $(TZ=GMT date +"%a, %d %b %Y %T %Z")
Location: /wait.html
Server: httpd
Status: 302 Moved Temporarily
"
reboot
%>
