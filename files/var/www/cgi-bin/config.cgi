#!/usr/bin/haserl
Date: <%= $(TZ=GMT0 date +"%a, %d %b %Y %T %Z" --date @$(( $(TZ=GMT0 date +%s) + 1000 ))) %>
Server: <%= $SERVER_SOFTWARE %>
Content-type: application/javascript; charset=UTF-8
Access-Control-Allow-Origin: *
Cache-Control: no-cache
Connection: close

<%
o=""
echo -n "readConfigYaml({"
for l in $(sed -n "/^\../p" p/mj.cgi|cut -d\| -f1); do
  d=${l%.*}; d=${d/./}; name=${l##*.}
  value=$(yaml-cli -g "$l")
  if [ "$o" != "$d" ]; then
    [ -n "$o" ] && echo -n "},"
    o="$d"
    echo -n "\"${d}\":{"
  else
    echo -n ","
  fi
  echo -n "\"${name}\":\"${value}\""
done
echo -n "}});"
%>
