#!/bin/sh

plugin="webhook"
source /usr/sbin/common-plugins

show_help() {
	echo "Usage: $0 [-u url] [-v] [-h]
  -u url      Webhook URL.
  -v          Verbose output.
  -h          Show this help.
"
	exit 0
}

# override config values with command line arguments
while getopts u:vh flag; do
	case ${flag} in
	u) webhook_url=${OPTARG} ;;
	v) verbose=1 ;;
	h) show_help ;;
	esac
done

[ "false" = "$webhook_enabled" ] && log "Sending to webhook is disabled." && exit 10

# validate mandatory values
[ -z "$webhook_url" ] && log "Webhook URL not found" && exit 11

command="curl --verbose"
command="${command} --connect-timeout ${curl_timeout}"
command="${command} --max-time ${curl_timeout} -X POST"

# SOCK5 proxy, if needed
if [ "true" = "$webhook_socks5_enabled" ]; then
	source /etc/webui/socks5.conf
	command="${command} --socks5-hostname ${socks5_host}:${socks5_port}"
	command="${command} --proxy-user ${socks5_login}:${socks5_password}"
fi

command="${command} --url ${webhook_url}"

log "$command"
eval "$command" >>$LOG_FILE 2>&1

[ "1" = "$verbose" ] && cat $LOG_FILE

exit 0
