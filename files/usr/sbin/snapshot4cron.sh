#!/bin/sh

snapshot="/tmp/snapshot4cron.jpg"
attempt=0
LIMIT_ATTEMPTS=5
SECONDS_TO_EXPIRE=120

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
    echo "Cannot get a snapshot. Maximum amount of retries reached."
    exit 1
  fi

  curl "http://127.0.0.1/image.jpg?t=$(date +"%s")" --output "$snapshot" --silent
  if [ $? -eq 0 ]; then
    echo "Snapshot saved to ${snapshot} at ${attempt} attempt."
    return
  fi

  echo "Cannot get a snapshot. Attempt ${attempt}."
  get_snapshot
}

while getopts fh flag; do
  case ${flag} in
  f) force=true ;;
  h) show_help ;;
  esac
done

if [ "true" = "$force" ]; then
  echo "Forced to comply."
  get_snapshot
elif [ ! -f "$snapshot" ]; then
  echo "Snapshot not found."
  get_snapshot
elif [ "$(date -r "$snapshot" +%s)" -le "$(( $(date +%s) - $SECONDS_TO_EXPIRE ))" ]; then
  echo "Snapshot is expired."
  get_snapshot
else
  echo "Snapshot is up to date."
fi
