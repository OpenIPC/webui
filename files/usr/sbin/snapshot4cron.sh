#!/bin/sh

plugin="snapshot"
source /usr/sbin/common-plugins
singleton

SNAPSHOT="/tmp/snapshot4cron.jpg"
SECONDS_TO_EXPIRE=120
LIMIT_ATTEMPTS=5

show_help() {
	echo "Usage: $0 [-f ] [-q] [-h]
  -f   Saving a new snapshot, no matter what.
  -q   Quiet output.
  -h   Show this help.
"
	exit 0
}

get_snapshot() {
	log "Trying to save a snapshot."
	LIMIT_ATTEMPTS=$(( $LIMIT_ATTEMPTS - 1 ))

	command="curl --max-time 5 --silent --fail --url http://127.0.0.1/image.jpg?t=$(date +"%s") --output ${SNAPSHOT}"
	log "$command"
	if $command >>$LOG_FILE; then
		log "Snapshot saved to ${SNAPSHOT}."
		quit_clean 0
	fi

	if [ "$LIMIT_ATTEMPTS" -le "0" ]; then
		log "Maximum amount of retries reached."
		quit_clean 2
	else
		log "${LIMIT_ATTEMPTS} attempts left."
		sleep 1
		get_snapshot
	fi
}

verbose=1
while getopts fhq flag; do
	case ${flag} in
	f) force=true ;;
	h) show_help ;;
	q) verbose=0 ;;
	esac
done

if [ "true" = "$force" ]; then
	log "Enforced run."
	get_snapshot
elif [ ! -f "$SNAPSHOT" ]; then
	log "Snapshot not found."
	get_snapshot
elif [ "$(date -r "$SNAPSHOT" +%s)" -le "$(( $(date +%s) - $SECONDS_TO_EXPIRE ))" ]; then
	log "Snapshot is expired."
	rm $SNAPSHOT
	get_snapshot
else
	log "Snapshot is up to date."
	sleep 2
	quit_clean 0
fi

exit 0
