#!/bin/sh

plugin="mqtt"
source /usr/sbin/common-plugins

show_help() {
	echo "Usage: $0 [-t topic] [-m message] [-s] [-v] [-h]
  -t topic    MQTT topic.
  -m message  Message playload.
  -s          Send a snapshot.
  -v          Verbose output.
  -h          Show this help.
"
	exit 0
}

# override config values with command line arguments
while getopts m:st:vh flag; do
	case ${flag} in
	m) mqtt_message=${OPTARG} ;;
	s) mqtt_send_snap="true" ;;
	t) mqtt_topic=${OPTARG} ;;
	v) verbose=1 ;;
	h) show_help ;;
	esac
done

[ "false" = "$mqtt_enabled" ] && log "Sending to MQTT broker is disabled." && exit 10

# validate mandatory values
[ -z "$mqtt_host" ] && log "MQTT broker host not found in config" && exit 11
[ -z "$mqtt_port" ] && log "MQTT broker port not found in config" && exit 12
[ -z "$mqtt_topic" ] && log "MQTT topic not found" && exit 13
[ -z "$mqtt_message" ] && log "MQTT message template not found" && exit 14
[ "true" = "$mqtt_send_snap" ] && [ -z "$mqtt_snap_topic" ] && log "MQTT topic for sending snapshot not found in config" && exit 15

# assign default values if not set
[ -z "$mqtt_client_id" ] && mqtt_client_id="${network_hostname}"

# parse strftime templates
mqtt_message=$(date +"$mqtt_message")

command="mosquitto_pub"
command="${command} -h ${mqtt_host}"
command="${command} -p ${mqtt_port}"
command="${command} -i ${mqtt_client_id}"

# MQTT credentials, if given
[ -n "$mqtt_username" ] && command="${command} -u ${mqtt_username}"
[ -n "$mqtt_password" ] && command="${command} -P ${mqtt_password}"

# SOCK5 proxy, if needed
if [ "true" = "$mqtt_socks5_enabled" ]; then
	source /etc/webui/socks5.conf
	socks_opts="--proxy socks5h://${socks5_login}:${socks5_password}@${socks5_host}:${socks5_port}"
fi
command="${command} ${socks_opts}"

# send text message
command1="${command} -t ${mqtt_topic} -m \"${mqtt_message}\""
log "$command1"
eval "$command1" >>$LOG_FILE 2>&1

# send file
if [ "true" = "$mqtt_send_snap" ]; then
	snapshot4cron.sh
	exitcode=$?
	[ $exitcode -ne 0 ] && log "Cannot get a snapshot. Exit code: $exitcode" && exit 2
	snapshot=/tmp/snapshot4cron.jpg
	[ ! -f "$snapshot" ] && log "Cannot find a snapshot" && exit 3
	mqtt_file=$snapshot
	command2="${command} -t ${mqtt_snap_topic} -f \"${mqtt_file}\""
	log "$command2"
	eval "$command2" >>$LOG_FILE 2>&1
fi

[ "1" = "$verbose" ] && cat $LOG_FILE

exit 0
