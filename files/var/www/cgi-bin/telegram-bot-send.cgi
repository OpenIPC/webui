#!/bin/sh

plugin="telegram"
config_file="/etc/${plugin}.cfg"
tmp_image="/tmp/telegram_snap.jpg"
ipaddr=$(printenv | grep HTTP_HOST | cut -d= -f2 | cut -d: -f1)
token=$(sed -n 1p ${config_file})
channel=$(sed -n 2p ${config_file})
hostname=$(hostname -s)
datetime=$(date +"%F %T")
epochtime=$(date +"%s")

echo "HTTP/1.1 200 OK"
echo "Date: $(TZ=GMT date +"%a, %d %b %Y %T %Z")"
echo "Content-Type: application/json; charset=utf-8"
echo "Server: httpd"
echo "Transfer-Encoding: chunked"
echo ""
echo "[]"

curl -s -k http://${ipaddr}/image.jpg?t=${epochtime} -o ${tmp_image} && \
  curl -s -k -X POST "https://api.telegram.org/bot${token}/sendPhoto?chat_id=${channel}" \
    -H "Content-Type: multipart/form-data" -F "photo=@${tmp_image}" -F "caption=${hostname}, ${datetime}" && \
  rm -rf ${tmp_image} 2>&1
