#!/bin/sh

config_file="/etc/webui/telegram.conf"
curl_timeout=100

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

# exit if plugin is not enabled and not ran with parameters
[ "$force" != "true" ] && [ "$telegram_enabled" != "true" ] && exit 0

snapshot="/tmp/${plugin}_snap.jpg"

# get image from camera
curl "http://127.0.0.1/image.jpg?t=$(date +"%s")" --output "$snapshot" --silent
if [ $? -eq 0 ]; then
  curl_options="--silent --insecure --connect-timeout ${curl_timeout} --max-time ${curl_timeout}"

  # SOCK5 proxy, if needed
  if [ "true" = "$telegram_socks5_enabled" ]; then
    include /etc/webui/socks5.conf
    curl_options="${curl_options} --socks5-hostname ${socks5_server}:${socks5_port} --proxy-user ${socks5_login}:${socks5_password}"
  fi

  url="https://api.telegram.org/bot${telegram_token}/sendPhoto?chat_id=${telegram_channel}"
  result=$(curl $curl_options --request POST $url -H "Content-Type: multipart/form-data" -F "photo=@${snapshot}" -F "caption=$(hostname -s), $(date +"%F %T")")
  if [ "${result:1:6}" = '"ok":f' ]; then
    echo "Cannot post snapshot to Telegram."
    echo $result
    exit 1
  fi
  rm -f $snapshot
else
  echo "Cannot get a snapshot."
  exit 1
fi

exit 0
