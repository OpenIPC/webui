#!/bin/sh

plugin="ntfy"

. /usr/sbin/common-plugins

show_help() {
	echo "Usage: $0 [-s server_url] [-p port] [-t topic] [-s subject] [-b body] [-u user -l login] [-v] [-h]
  -d server   Domain URL or IP of server
  -p port     Server port
  -t topic    NTFY message topic
  -s subject  Subject or title of notification
  -b body     notification body
  -u user
  -l login
  -v          Verbose output.
  -h          Show this help.
"
	exit 0
}

# override config values with command line arguments
while getopts s:p:t:s:b:u:l:vh flag; do
	case "$flag" in
		d)
			ntfy_url=$OPTARG
			;;
		p)
			ntfy_port=$OPTARG
			;;
		t)
			ntfy_topic=$OPTARG
			;;
		u)
			ntfy_user=$OPTARG
			;;
		l)
			ntfy_password=$OPTARG
			;;
		s)
			ntfy_msg_title=$OPTARG
			;;
		b)
			ntfy_msg_body=$OPTARG
			;;
		v)
			verbose="true"
			;;
		h|*)
			show_help
			;;
	esac
done

[ "false" = "$ntfy_enabled" ] && log "Sending to NTFY is disabled." && exit 10

# validate mandatory values
[ -z "$ntfy_url" ] && log "NTFY url not found in config" && exit 11
[ -z "$ntfy_port" ] && log "NTFY port not found in config" && exit 12
[ -z "$ntfy_topic" ] && log "NTFY topic not found in config" && exit 13

# assign default values if not set
[ -z "$ntfy_msg_body" ] && ntfy_msg_body="test message"

command="curl --silent --verbose -XPOST"
command="${command} --connect-timeout ${curl_timeout}"
command="${command} --max-time ${curl_timeout}"

if [ ! -z "$ntfy_username" ] && [ ! -z "$ntfy_password" ]; then		# if login is specified add it
	command="${command} -u $ntfy_username:$ntfy_password"
fi

if [ ! -z "$ntfy_msg_title" ]; then			# if title is specified add it
	command="${command} -H \"Title:$ntfy_msg_title\""
fi
command="${command} -H \"X-Priority: $ntfy_msg_priority\""
command="${command} -H \"Message: ${ntfy_msg_body}\""

if [ "true" == "$ntfy_attach_snapshot" ]; then
	snapshot=/tmp/snapshot4cron.jpg
	snapshot4cron.sh
	command="${command} -T ${snapshot} -H \"Filename: snapshot.jpg\""
fi

command="${command} ${ntfy_url}:${ntfy_port}/${ntfy_topic}"

log "$command"
eval "$command" >>"$LOG_FILE" 2>&1

[ "true" = "$verbose" ] && cat "$LOG_FILE"

exit 0
