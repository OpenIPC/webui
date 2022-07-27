#!/bin/sh

plugin="telegram"
config_file="/etc/webui/${plugin}.conf"
curl_timeout=100

mkdir -p /tmp/webui

if [ -n "$1" ] && [ -n "$2" ]; then
  force="true"
  telegram_channel="$1"
  telegram_token="$2"
else
  # read variables from config
  [ -f "$config_file" ] && source $config_file
fi

if [ -z "$telegram_channel" ] || [ -z "$telegram_token" ]; then
  echo -e "Usage: $0 <channel-id> <token>\n or create ${config_file} config file."
  exit 1
fi

if [ "true" != "$telegram_enabled" ] && [ "true" != "$force" ]; then
  echo "Sending to Telegram is not enabled."
  exit 10
fi

# validate mandatory values
[ -z "$telegram_token"   ] && echo -e "Telegram token not found in config" && exit 11
[ -z "$telegram_channel" ] && echo -e "Telegram channel not found in config" && exit 12

curl_options="--verbose --silent --insecure --connect-timeout ${curl_timeout} --max-time ${curl_timeout}"

# SOCK5 proxy, if needed
if [ "true" = "$telegram_socks5_enabled" ]; then
  include /etc/webui/socks5.conf
  curl_options="${curl_options} --socks5-hostname ${socks5_host}:${socks5_port} --proxy-user ${socks5_login}:${socks5_password}"
fi

url="https://api.telegram.org/bot${telegram_token}/sendPhoto?chat_id=${telegram_channel}"

snapshot="/tmp/${plugin}_snap.jpg"

# get image from camera
curl "http://127.0.0.1/image.jpg?t=$(date +"%s")" --output "$snapshot" --silent
if [ $? -eq 0 ]; then
  :>/tmp/webui/${plugin}.log
  cmd="curl ${curl_options} --request POST ${url} -H \"Content-Type: multipart/form-data\" -F \"photo=@${snapshot}\" -F \"caption=$(hostname -s), $(date +"%F %T")\""
  echo "$cmd" >>/tmp/webui/${plugin}.log
  result="$($cmd 2>&1)"
  echo "$result" >>/tmp/webui/${plugin}.log
  if [ "${result:1:6}" = '"ok":f' ]; then
    echo "Cannot post snapshot to Telegram."
    echo "$result"
    exit 1
  fi
  rm -f ${snapshot}
else
  echo "Cannot get a snapshot."
  exit 2
fi

exit 0
