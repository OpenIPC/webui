#!/usr/bin/haserl
<%
/usr/sbin/ntpd -q -d -n

echo "HTTP/1.1 302 Moved Temporarily"
echo "Content-type: text/html; charset=UTF-8"
echo "Date: $(TZ=GMT date +"%a, %d %b %Y %T %Z")"
echo "Location: /cgi-bin/status.cgi"
echo "Server: httpd"
echo "Status: 302 Moved Temporarily"
%>
