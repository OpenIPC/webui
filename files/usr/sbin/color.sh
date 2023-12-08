#!/bin/sh

# set parameters from cli, if empty
[ -z "$mode" ] && mode=$1

MODE_FILE=/tmp/nightmode.txt

vendor=$(ipcinfo --vendor)

case "$1" in
	off)
		case "$vendor" in
			ingenic)
				/usr/sbin/imp-control.sh ispmode 1
				;;
			*)
				curl http://127.0.0.1/night/on
				;;
		esac
		echo "night" >$MODE_FILE
		;;
	on)
		case "$vendor" in
			ingenic)
				/usr/sbin/imp-control.sh ispmode 0
				;;
			*)
				curl http://127.0.0.1/night/off
				;;
		esac
		echo "day" >$MODE_FILE
		;;
	*)
		echo "Unknown mode"
		exit 1
		;;
esac

exit 0