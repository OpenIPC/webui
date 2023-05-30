#!/bin/sh

plugin="speaker"
source /usr/sbin/common-plugins

SUPPORTED="goke hisilicon"
[ -z "$(echo $SUPPORTED | sed -n "/\b$(ipcinfo --vendor)\b/p")" ] &&
	log "Playing on speaker is not supported on your camera!" && exit 1

show_help() {
	echo "Usage: $0 [-u url] [-f file] [-v] [-h]
  -u url      Audio URL.
  -f file     Audio file.
  -v          Verbose output.
  -h          Show this help.
"
	exit 0
}

# override config values with command line arguments
while getopts f:u:vh flag; do
	case ${flag} in
	f) speaker_file=${OPTARG} ;;
	u) speaker_url=${OPTARG} ;;
	v) verbose=1 ;;
	h) show_help ;;
	esac
done

[ "false" = "$speaker_enabled" ] &&
	log "Playing on speaker is disabled in config ${config_file}." && exit 10

[ "false" = "$(yaml-cli -g .audio.enabled)" ] &&
	log "Playing on speaker is disabled in Majestic." && exit 11

# validate mandatory values
[ -z "$speaker_url" ] &&
	log "Speaker URL is not set" && exit 12
[ -z "$speaker_file" ] &&
	log "Audio file is not set" && exit 13
[ ! -f "$speaker_file" ] &&
	log "Audio file ${speaker_file} not found" && exit 14

command="curl --verbose"
command="${command} --connect-timeout ${curl_timeout}"
command="${command} --max-time ${curl_timeout} -X POST"
command="${command} -T ${speaker_file}"
command="${command} --url ${speaker_url}"

log "$command"
eval "$command" >>$LOG_FILE 2>&1

[ "1" = "$verbose" ] && cat $LOG_FILE

exit 0
