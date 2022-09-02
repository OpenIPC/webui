#!/bin/sh

plugin="webhook"
config_file="/etc/webui/${plugin}.conf"
curl_timeout=100

log_file=/tmp/webui/${plugin}.log
mkdir -p $(dirname $log_file)
:>$log_file

show_help() {
  echo "Usage: $0 [-u url] [-v] [-h]
  -u url      Webhook URL.
  -v          Verbose output.
  -h          Show this help.
"
  exit 0
}

# read variables from config
[ -f "$config_file" ] && source $config_file

# override config values with command line arguments
while getopts u:vh flag; do
  case ${flag} in
  u) webhook_url=${OPTARG} ;;
  v) verbose=1 ;;
  h) show_help ;;
  esac
done

[ "false" = "$webhook_enabled" ] &&
  echo "Sending to webhook is disabled." && exit 10

# validate mandatory values
[ -z "$webhook_url" ] &&
  echo "Webhook URL not found" && exit 11

command="curl"
[ "1" = "$verbose" ] && command="${command} --verbose"
command="${command} --connect-timeout ${curl_timeout}"
command="${command} --max-time ${curl_timeout}"

# SOCK5 proxy, if needed
if [ "true" = "$webhook_socks5_enabled" ]; then
  source /etc/webui/socks5.conf
  command="${command} --socks5-hostname ${socks5_host}:${socks5_port}"
  command="${command} --proxy-user ${socks5_login}:${socks5_password}"
fi

command="${command} --url ${webhook_url}"

echo "$command" >>$log_file
eval "$command" >>$log_file 2>&1

[ "1" = "$verbose" ] && cat $log_file

exit 0
