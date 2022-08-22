#!/bin/sh

plugin="telegram"
config_file="/etc/webui/${plugin}.conf"
curl_timeout=100

log_file=/tmp/webui/${plugin}.log
mkdir -p $(dirname $log_file)
:>$log_file

show_help() {
  echo "Usage: $0 [-t token] [-c channel] [-m message] [-p photo] [-s] [-b] [-v] [-h]
  -t token    Telegram bot token. See https://t.me/botfather if you need one.
  -c channel  Telegram channel ID. See https://gist.github.com/mraaroncruz/e76d19f7d61d59419002db54030ebe35
  -m message  Message text.
  -p photo    Path to photo file.
  -s          Disable notification.
  -v          Verbose output.
  -h          Show this help.
"
  exit 0
}

# read variables from config
[ -f "$config_file" ] && source $config_file

# default values
telegram_disable_notification=false

# override config values with command line arguments
while getopts c:m:p:st:vh flag; do
  case ${flag} in
  c) telegram_channel=${OPTARG} ;;
  m) telegram_message=${OPTARG} ;;
  p) telegram_photo=${OPTARG} ;;
  s) telegram_disable_notification=true ;;
  t) telegram_token=${OPTARG} ;;
  v) verbose=1 ;;
  h) show_help ;;
  esac
done

[ "false" = "$telegram_enabled" ] &&
  echo "Sending to Telegram is disabled." && exit 10

# validate mandatory values
[ -z "$telegram_token" ] &&
  echo "Telegram token not found" && exit 11
[ -z "$telegram_channel" ] &&
  echo "Telegram channel not found" && exit 12

if [ -z "$telegram_message" ]; then
  telegram_message="$(hostname -s), $(date +"%F %T")"

  if [ -z "$telegram_photo" ]; then
    snapshot4cron.sh
    [ $? -ne 0 ] && echo "Cannot get a snapshot" && exit 2
    snapshot=/tmp/snapshot4cron.jpg
    [ ! -f "$snapshot" ] && echo "Cannot find a snapshot" && exit 3
    telegram_photo=$snapshot
  fi
fi

command="curl --silent" # --insecure
[ "1" = "$verbose" ] && command="${command} --verbose"
command="${command} --connect-timeout ${curl_timeout}"
command="${command} --max-time ${curl_timeout}"

# SOCK5 proxy, if needed
if [ "true" = "$telegram_socks5_enabled" ]; then
  source /etc/webui/socks5.conf
  command="${command} --socks5-hostname ${socks5_host}:${socks5_port}"
  command="${command} --proxy-user ${socks5_login}:${socks5_password}"
fi

command="${command} --url https://api.telegram.org/bot${telegram_token}/"
if [ -n "$telegram_photo" ]; then
  command="${command}sendPhoto"
  command="${command} -F 'photo=@${telegram_photo}'"
  command="${command} -F 'caption=${telegram_message}'"
else
  command="${command}sendMessage"
  command="${command} -F 'text=${telegram_message}'"
fi
command="${command} -H 'Content-Type: multipart/form-data'"
command="${command} -F 'chat_id=${telegram_channel}'"
command="${command} -F 'disable_notification=${telegram_disable_notification}'"

echo "$command" >>$log_file
eval "$command" >>$log_file 2>&1

[ "1" = "$verbose" ] && cat $log_file

exit 0
