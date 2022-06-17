#!/bin/sh

config_file="/etc/telegram.cfg"

if [ -n "$1" ] && [ -n "$2" ]; then
  channel=${1}
  token=${2}
else
  if [ -f "$config_file" ]; then
    token=$(sed -n 1p $config_file)
    channel=$(sed -n 2p $config_file)
  else
    echo -e "Usage: $0 <channel-id> <token>\n or create ${config_file} config file."
    exit 1
  fi
fi

hostname=$(hostname -s)
datetime=$(date +"%F %T")
epochtime=$(date +"%s")
snapshot="/tmp/telegram_snap.jpg"

if curl -s -k http://127.0.0.1/image.jpg?t=${epochtime} -o ${snapshot}
then
  result=$(curl -s -k -X POST "https://api.telegram.org/bot${token}/sendPhoto?chat_id=${channel}" -H "Content-Type: multipart/form-data" -F "photo=@${snapshot}" -F "caption=${hostname}, ${datetime}")
  rm -rf ${snapshot}
  if [ "${result:1:6}" = '"ok":f' ]; then
    echo "Cannot post snapshot to Telegram."
    exit 1
  fi
else
  echo "Cannot get a snapshot."
  exit 1
fi

exit 0
