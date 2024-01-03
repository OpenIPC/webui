#!/bin/sh

plugin="motion"

. /usr/sbin/common-plugins
singleton

STOP_FILE=/tmp/motion.stop
UNSUPPORTED="hi3516cv100 hi3516av100"

if [ -n "$(echo $UNSUPPORTED | sed -n "/\b$(ipcinfo --family)\b/p")" ]; then
	log "Motion detection is not supported on your camera!"
	 quit_clean 1
 fi

if [ "true" != "$motion_enabled" ]; then
	log "Motion detection is disabled in config!"
	quit_clean 3
fi

# throttle execution
[ -z "$motion_throttle" ] && motion_throttle=1

if [ -f "$STOP_FILE" ]; then
	if [ "$(date -r "$STOP_FILE" +%s)" -ge "$(( $(date +%s) - motion_throttle ))" ]; then
		log "Too soon for another trigger!"
		quit_clean 99
	fi
fi

# check number of the motions detected
if [ "$1" -lt "$motion_sensitivity" ]; then
	log "Number of objects is below sensitivity threshold!"
	quit_clean 4
fi

touch "$STOP_FILE"

# get a fresh snapshot
snapshot4cron.sh -f
if [ $? -ne 0 ]; then
	echo "Cannot get a snapshot"
	quit_clean 2
fi

# send alerts
[ "true" = "$motion_send2email"    ] && send2email.sh
[ "true" = "$motion_send2ftp"      ] && send2ftp.sh
[ "true" = "$motion_send2mqtt"     ] && send2mqtt.sh
[ "true" = "$motion_send2telegram" ] && send2telegram.sh
[ "true" = "$motion_send2webhook"  ] && send2webhook.sh
[ "true" = "$motion_send2yadisk"   ] && send2yadisk.sh
[ "true" = "$motion_playonspeaker" ] && playonspeaker.sh
