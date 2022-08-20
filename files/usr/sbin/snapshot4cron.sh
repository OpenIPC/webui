#!/bin/sh

snapshot="/tmp/snapshot4cron.jpg"
attempt=0
LIMIT_ATTEMPTS=5
SECONDS_TO_EXPIRE=120
LOG_FILE=/tmp/snapshot4cron.log
LOCK_FILE=/tmp/snapshot4cron.lock

PID=$$

log() {
  echo "$(date +%s) [${PID}] ${1}" >>$LOG_FILE
  echo "$1"
}

show_help() {
  echo "Usage: $0 [-f ] [-h]
  -f   Saving a new snapshot, no matter what.
  -h   Show this help.
"
  exit 0
}

get_snapshot() {
  attempt=$(( $attempt + 1 ))
  if [ "$attempt" -ge "$LIMIT_ATTEMPTS" ]; then
    log "Cannot get a snapshot. Maximum amount of retries reached."
    rm "$LOCK_FILE"
    exit 1
  fi

  curl "http://127.0.0.1/image.jpg?t=$(date +"%s")" --output "$snapshot" --silent
  if [ $? -eq 0 ]; then
    log "Snapshot saved to ${snapshot} at ${attempt} attempt."
    return
  fi

  log "Cannot get a snapshot. Attempt ${attempt}."
  get_snapshot
}

while getopts fh flag; do
  case ${flag} in
  f) force=true ;;
  h) show_help ;;
  esac
done

if [ -f "$LOCK_FILE" ] && [ "true" != "$force" ]; then
  log "Another process is running. Exiting."
  exit 1
fi

touch "$LOCK_FILE"

log "$0 started."

if [ "true" = "$force" ]; then
  log "Forced to comply."
  get_snapshot
elif [ ! -f "$snapshot" ]; then
  log "Snapshot not found."
  get_snapshot
elif [ "$(date -r "$snapshot" +%s)" -le "$(( $(date +%s) - $SECONDS_TO_EXPIRE ))" ]; then
  log "Snapshot is expired."
  get_snapshot
else
  log "Snapshot is up to date."
fi

log "$0 finished."

rm "$LOCK_FILE"

exit 0
