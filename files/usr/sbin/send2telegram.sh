#!/bin/sh

config_file="/etc/telegram.cfg"

if [ -n "$1" ] && [ -n "$2" ]; then
  force="true"
  telegram_channel="$1"
  telegram_token="$2"
else
  # read variables from config
  eval $(grep = $config_file)
fi

if [ -z "$telegram_channel" ] || [ -z "$telegram_token" ]; then
  echo -e "Usage: $0 <channel-id> <token>\n or create ${config_file} config file."
  exit 1
fi

# exit if plugin is not enabled and not ran with parameters
[ "$force" != "true" ] && [ "$telegram_enabled" != "true" ] && exit 0

hostname=$(hostname -s)
datetime=$(date +"%F %T")
epochtime=$(date +"%s")
snapshot="/tmp/telegram_snap.jpg"

curl -s -k http://127.0.0.1/image.jpg?t=${epochtime} -o $snapshot
if [ $? -eq 0 ]; then
  ls -l $snapshot
  result=$(curl --silent --insecure -X POST "https://api.telegram.org/bot${telegram_token}/sendPhoto?chat_id=${telegram_channel}" -H "Content-Type: multipart/form-data" -F "photo=@${snapshot}" -F "caption=${hostname}, ${datetime}")
  rm -f $snapshot
  if [ "${result:1:6}" = '"ok":f' ]; then
    echo "Cannot post snapshot to Telegram."
    echo $result
    exit 1
  fi
else
  echo "Cannot get a snapshot."
  exit 1
fi

exit 0
