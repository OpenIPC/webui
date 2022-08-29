#!/bin/sh

SNAPSHOT="/tmp/snapshot4cron.jpg"
SECONDS_TO_EXPIRE=120
LOG_FILE=/tmp/snapshot4cron.log
LOCK_FILE=/tmp/snapshot4cron.lock
LIMIT_ATTEMPTS=5
attempt=0

PID=$$

log() {
  echo "$(date +%s) [${PID}] ${1}" >>$LOG_FILE
  [ "1" != "$quiet" ] && echo "$1"
}

clean_quit() {
  rm "$LOCK_FILE"
  exit $1
}

show_help() {
  echo "Usage: $0 [-f ] [-v] [-h]
  -f   Saving a new snapshot, no matter what.
  -q   Quiet output.
  -h   Show this help.
"
  exit 0
}

get_snapshot() {
	touch "$LOCK_FILE"

  attempt=$(( $attempt + 1 ))
  if [ "$attempt" -gt "$LIMIT_ATTEMPTS" ]; then
    log "Maximum amount of retries reached."
    clean_quit 1
  fi

  log "Attempt ${attempt}."
  if curl --silent --fail --url http://127.0.0.1/image.jpg?t=$(date +"%s") --output ${SNAPSHOT} >>$LOG_FILE; then
    log "Snapshot saved to ${SNAPSHOT} at ${attempt} attempt."
    clean_quit 0
  fi

  log "Cannot get a snapshot."
  get_snapshot
}

while getopts fhv flag; do
  case ${flag} in
  f) force=true ;;
  h) show_help ;;
  q) quiet=1 ;;
  esac
done

if [ -f "$LOCK_FILE" ] && [ "true" != "$force" ]; then
  log "Another process is running."
  _a=0
  while [ ! -f "$SNAPSHOT" ]; do
    echo "Waiting for a snapshot."
    _a=$(( $_a + 1 ))
    [ "$_a" -ge "5" ] && log "Maximum waiting time reached." && exit 2
    sleep 1
  done
  exit 0
fi

if [ "true" = "$force" ]; then
  log "Forced to comply."
  get_snapshot
elif [ ! -f "$SNAPSHOT" ]; then
  log "Snapshot not found."
  get_snapshot
elif [ "$(date -r "$SNAPSHOT" +%s)" -le "$(( $(date +%s) - $SECONDS_TO_EXPIRE ))" ]; then
  log "Snapshot is expired."
  get_snapshot
else
  log "Snapshot is up to date."
  exit 0
fi
