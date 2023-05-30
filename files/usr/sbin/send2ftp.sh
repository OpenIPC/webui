#!/bin/sh

plugin="ftp"
source /usr/sbin/common-plugins

show_help() {
	echo "Usage: $0 [-h host] [-p port] [-u username] [-P password] [-d path] [-f file] [-v] [-h]
  -s host     FTP server FQDN or IP address.
  -p port     FTP server port.
  -d path     Directory on server, relative to FTP root.
  -f file     File to upload.
  -u username FTP username.
  -P password FTP password.
  -v          Verbose output.
  -h          Show this help.
"
	exit 0
}

# override config values with command line arguments
while getopts d:f:p:P:s:u:vh flag; do
	case ${flag} in
	d) ftp_path=${OPTARG} ;;
	f) ftp_file=${OPTARG} ;;
	p) ftp_port=${OPTARG} ;;
	P) ftp_password=${OPTARG} ;;
	s) ftp_host=${OPTARG} ;;
	u) ftp_username=${OPTARG} ;;
	v) verbose=1 ;;
	h) show_help ;;
	esac
done

[ "false" = "$ftp_enabled" ] &&
	log "Sending to FTP is disabled." && exit 10

# validate mandatory values
[ -z "$ftp_host" ] &&
	log "FTP host not found" && exit 11
[ -z "$ftp_port" ] &&
	log "FTP port not found" && exit 12

if [ -z "$ftp_file" ]; then
	snapshot4cron.sh
	# [ $? -ne 0 ] && echo "Cannot get a snapshot" && exit 2
	snapshot=/tmp/snapshot4cron.jpg
	[ ! -f "$snapshot" ] && log "Cannot find a snapshot" && exit 3

	ftp_file=$snapshot
fi

command="curl --verbose"
command="${command} --connect-timeout ${curl_timeout}"
command="${command} --max-time ${curl_timeout}"

# SOCK5 proxy, if needed
if [ "true" = "$ftp_socks5_enabled" ]; then
	source /etc/webui/socks5.conf
	command="${command} --socks5-hostname ${socks5_host}:${socks5_port}"
	command="${command} --proxy-user ${socks5_login}:${socks5_password}"
fi

command="${command} --url ftp://"
[ -n "$ftp_username" ] && [ -n "$ftp_password" ] && command="${command}${ftp_username}:${ftp_password}"
command="${command}@${ftp_host}:${ftp_port}"
[ -n "$ftp_path" ] && command="${command}/${ftp_path// /%20}"
command="${command}/$(date +"$ftp_template")"
command="${command} --upload-file ${ftp_file}"
command="${command} --ftp-create-dirs"

log "$command"
eval "$command" >>$LOG_FILE 2>&1

[ "1" = "$verbose" ] && cat $LOG_FILE

exit 0
