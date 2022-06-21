#!/bin/sh
http_date='%a, %d %b %Y %T %Z'
timenow="$(TZ=GMT0 date +'%a, %d %b %Y %T %Z' \@$(echo $(date +%s)+1000|bc))"

echo "Content-Type: application/javascript; charset=UTF-8
Access-Control-Allow-Origin: *
Cache-Control: no-cache
Connection: close
Date: ${timenow}
"
echo -n "readConfigYaml({ "
olddomain=""
for line in $(sed -n "/^\../p" _mj.cgi|cut -d\| -f1); do
  domain=${line%.*}
  domain=${domain/./}  # POSIX: domain=$(echo "$domain"|sed 's/^\.//')
  name=${line##*.}
  value=$(yaml-cli -g "$line")
  if [ "$olddomain" != "$domain" ]; then
    [ -n "$olddomain" ] && echo -n "},"
    olddomain="$domain"
    echo -n "\"${domain}\":{"
  else
    echo -n ","
  fi
  echo -n "\"${name}\":\"${value}\""
done
echo -n "}});"
