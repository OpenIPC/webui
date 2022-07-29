#!/bin/sh

plugin="telegram"
config_file="/etc/webui/${plugin}.conf"
curl_timeout=100

show_help() {
  echo "Usage: $0 [-t token] [-c channel] [-m message] [-p photo] [-s] [-h]"
  echo "  -t token    Telegram bot token. See https://t.me/botfather if you need one."
  echo "  -c channel  Telegram channel ID. See https://gist.github.com/mraaroncruz/e76d19f7d61d59419002db54030ebe35"
  echo "  -m message  Message text."
  echo "  -p photo    Path to photo file."
  echo "  -s          Disable notification."
  echo "  -h          Show this help."
  exit 0
}

mkdir -p /tmp/webui

# read variables from config
[ -f "$config_file" ] && source $config_file

# default values
telegram_disable_notification=false

# override config values with command line arguments
while getopts c:m:p:st:h flag; do
  case ${flag} in
    c) telegram_channel=${OPTARG};;
    m) telegram_message=${OPTARG};;
    p) telegram_photo=${OPTARG};;
    s) telegram_disable_notification=true;;
    t) telegram_token=${OPTARG};;
    h) show_help;;
  esac
done

if [ "false" = "$telegram_enabled" ]; then
  echo "Sending to Telegram is not enabled."
  exit 10
fi

# validate mandatory values
[ -z "$telegram_token"   ] && echo -e "Telegram token not found" && exit 11
[ -z "$telegram_channel" ] && echo -e "Telegram channel not found" && exit 12

if [ -z "$telegram_message" ]; then
  telegram_message="$(hostname -s), $(date +"%F %T")"

  if [ -z "$telegram_photo" ]; then
    snapshot="/tmp/${plugin}_snap.jpg"
    curl "http://127.0.0.1/image.jpg?t=$(date +"%s")" --output "$snapshot" --silent
    [ $? -ne 0 ] && echo "Cannot get a snapshot." && exit 2
    telegram_photo=$snapshot
  fi
fi

curl_options="--silent --verbose --insecure --connect-timeout ${curl_timeout} --max-time ${curl_timeout}"

# SOCK5 proxy, if needed
if [ "true" = "$telegram_socks5_enabled" ]; then
  include /etc/webui/socks5.conf
  curl_options="${curl_options} --socks5-hostname ${socks5_host}:${socks5_port} --proxy-user ${socks5_login}:${socks5_password}"
fi

command="curl ${curl_options} --url https://api.telegram.org/bot${telegram_token}/"
if [ -n "$telegram_photo" ]; then
  command="${command}sendPhoto -H 'Content-Type: multipart/form-data' -F 'chat_id=${telegram_channel}' -F 'photo=@${telegram_photo}' -F 'caption=${telegram_message}' -F 'disable_notification=${telegram_disable_notification}'"
else
  command="${command}sendMessage -H 'Content-Type: multipart/form-data' -F 'chat_id=${telegram_channel}' -F 'text=${telegram_message}' -F 'disable_notification=${telegram_disable_notification}'"
fi
echo "$command" >/tmp/webui/${plugin}.log
eval "$command" >>/tmp/webui/${plugin}.log 2>&1
[ -f ${snapshot} ] && rm -f ${snapshot}

exit 0
