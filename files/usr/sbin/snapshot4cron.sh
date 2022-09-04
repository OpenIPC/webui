#!/bin/sh

log() {
  _txt="$(date +%s) [${PID}] ${1}"
  echo "$_txt" >>$LOG_FILE
  [ "1" != "$quiet" ] && echo "$_txt"
  unset _txt
}

clean_quit() {
  [ -f "$LOCK_FILE" ] && rm "$LOCK_FILE"
  log "Exiting"
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
  log "Trying to save a snapshot."
  LIMIT_ATTEMPTS=$(( $LIMIT_ATTEMPTS - 1 ))

  if curl --silent --fail --url http://127.0.0.1/image.jpg?t=$(date +"%s") --output ${SNAPSHOT} >>$LOG_FILE; then
    log "Snapshot saved to ${SNAPSHOT}."
    clean_quit 0
  fi

  if [ "$LIMIT_ATTEMPTS" -le "0" ]; then
    log "Maximum amount of retries reached."
    clean_quit 2
  else
    log "${LIMIT_ATTEMPTS} attempts left."
    sleep 1
    get_snapshot
  fi
}

LOG_FILE=/tmp/snapshot4cron.log
LOCK_FILE=/var/run/snapshot4cron.pid
SNAPSHOT="/tmp/snapshot4cron.jpg"
SECONDS_TO_EXPIRE=120
PID=$$
LIMIT_ATTEMPTS=5

if [ -f "$LOCK_FILE" ] && ps | grep "^\s*\b$(cat "$LOCK_FILE")\b" >/dev/null; then
  log "Another instance running."
  clean_quit 1
fi
printf "$PID" >$LOCK_FILE

while getopts fhv flag; do
  case ${flag} in
  f) force=true ;;
  h) show_help ;;
  q) quiet=1 ;;
  esac
done

if [ "true" = "$force" ]; then
  log "Enforsed run."
  get_snapshot
elif [ ! -f "$SNAPSHOT" ]; then
  log "Snapshot not found."
  get_snapshot
elif [ "$(date -r "$SNAPSHOT" +%s)" -le "$(( $(date +%s) - $SECONDS_TO_EXPIRE ))" ]; then
  log "Snapshot is expired."
  get_snapshot
else
  log "Snapshot is up to date."
  clean_quit 0
fi
