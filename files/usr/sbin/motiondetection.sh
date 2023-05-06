#!/bin/sh

plugin="motion"
source /usr/sbin/common-plugins
singleton

UNSUPPORTED="hi3516cv100 hi3516av100"
[ -n "$(echo $UNSUPPORTED | sed -n "/\b$(ipcinfo --family)\b/p")" ] &&
  log "Motion detection is not supported on your camera!" && quit_clean 1

[ "true" != "$motion_enabled" ] &&
  log "Motion detection is disabled in config!" && quit_clean 3

STOP_FILE=/tmp/motion.stop
TEMPLATE="Motion detected in \d* regions"

logread -f | while read line; do
   output=$(echo $line | grep -o "$TEMPLATE" | cut -d' ' -f4)
   if ! [[ "$output" =~ ^[0-9]{1,2}$ ]]; then
      continue
   fi
   if [ "$output" -lt "$((51 - $motion_sensitivity))" ]; then
      continue
   fi

  # throttle execution
  [ -f "$STOP_FILE" ] && [ "$(date -r "$STOP_FILE" +%s)" -ge "$(($(date +%s) - $motion_throttle))" ] && continue
  touch "$STOP_FILE"

  # get a fresh snapshot
  snapshot4cron.sh -f
  [ $? -ne 0 ] && echo "Cannot get a snapshot" && quit_clean 2

  # send alerts
  [ "true" = "$motion_send2email" ] && send2email.sh
  [ "true" = "$motion_send2ftp" ] && send2ftp.sh
  [ "true" = "$motion_send2mqtt" ] && send2mqtt.sh
  [ "true" = "$motion_send2telegram" ] && send2telegram.sh
  [ "true" = "$motion_send2webhook" ] && send2webhook.sh
  [ "true" = "$motion_send2yadisk" ] && send2yadisk.sh
  [ "true" = "$motion_playonspeaker" ] && playonspeaker.sh
done
