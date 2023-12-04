#!/bin/sh

plugin="webhook"

. /usr/sbin/common-plugins

show_help() {
	echo "Usage: $0 [-u url] [-v] [-h]
  -u url      Webhook URL.
  -r          Use HEIF image format.
  -v          Verbose output.
  -h          Show this help.
"
	exit 0
}

# override config values with command line arguments
while getopts u:vh flag; do
	case ${flag} in
	r) webhook_use_heif="true" ;;
	u) webhook_url=${OPTARG} ;;
	v) verbose="true" ;;
	h) show_help ;;
	esac
done

[ "false" = "$webhook_enabled" ] && log "Sending to webhook is disabled." && exit 10

# validate mandatory values
[ -z "$webhook_url" ] && log "Webhook URL not found" && exit 11

command="curl --verbose"
command="${command} --connect-timeout ${curl_timeout}"
command="${command} --max-time ${curl_timeout} -X POST"

if [ "true" = "$webhook_attach_snapshot" ]; then
	if [ "true" = "$webhoook_use_heif" ] && [ "h265" = "$(yaml-cli -g .video0.codec)" ]; then
		snapshot=/tmp/snapshot4cron.heif
		snapshot4cron.sh -r
	else
		snapshot=/tmp/snapshot4cron.jpg
		snapshot4cron.sh
	fi
	exitcode=$?
	[ $exitcode -ne 0 ] && log "Cannot get a snapshot. Exit code: $exitcode" && exit 2
	snapshot=/tmp/snapshot4cron.jpg
	[ ! -f "$snapshot" ] && log "Cannot find a snapshot" && exit 3
	command="${command} -F 'image=@$snapshot'"
fi

# SOCK5 proxy, if needed
if [ "true" = "$webhook_socks5_enabled" ]; then
	. /etc/webui/socks5.conf
	command="${command} --socks5-hostname ${socks5_host}:${socks5_port}"
	command="${command} --proxy-user ${socks5_login}:${socks5_password}"
fi

command="${command} --url ${webhook_url}"

log "$command"
eval "$command" >>$LOG_FILE 2>&1

[ "true" = "$verbose" ] && cat $LOG_FILE

exit 0
