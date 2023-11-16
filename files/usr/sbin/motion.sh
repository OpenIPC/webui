#!/bin/sh

plugin="motion"
source /usr/sbin/common-plugins
singleton

STOP_FILE=/tmp/motion.stop
UNSUPPORTED="hi3516cv100 hi3516av100"

[ -n "$(echo $UNSUPPORTED | sed -n "/\b$(ipcinfo --family)\b/p")" ] &&
	log "Motion detection is not supported on your camera!" && quit_clean 1

[ "true" != "$motion_enabled" ] &&
	log "Motion detection is disabled in config!" && quit_clean 3

# throttle execution
[ -z "$motion_throttle" ] && motion_throttle=1
[ -f "$STOP_FILE" ] && [ "$(date -r "$STOP_FILE" +%s)" -ge "$(($(date +%s) - $motion_throttle))" ] &&
	log "Too soon for another trigger!" && quit_clean 99

# check number of the motions detected
[ "$1" -lt "$motion_sensitivity" ] &&
	log "Number of objects is below sensitivity threshold!" && quit_clean 4

touch "$STOP_FILE"

# get a fresh snapshot
snapshot4cron.sh -f
[ $? -ne 0 ] && echo "Cannot get a snapshot" && quit_clean 2

# send alerts
[ "true" = "$motion_send2email"    ] && send2email.sh
[ "true" = "$motion_send2ftp"      ] && send2ftp.sh
[ "true" = "$motion_send2mqtt"     ] && send2mqtt.sh
[ "true" = "$motion_send2telegram" ] && send2telegram.sh
[ "true" = "$motion_send2webhook"  ] && send2webhook.sh
[ "true" = "$motion_send2yadisk"   ] && send2yadisk.sh
[ "true" = "$motion_playonspeaker" ] && playonspeaker.sh
