#!/bin/sh

# set parameters from cli, if empty
[ -z "$mode" ] && mode=$1

MODE_FILE=/tmp/colormode.txt

vendor=$(ipcinfo --vendor)

switch_to_color() {
	case "$vendor" in
		ingenic)
			/usr/sbin/imp-control.sh ispmode 0
			;;
		*)
			curl http://127.0.0.1/night/off
			;;
	esac
	echo "Switched to full-color mode"
	echo "day" >$MODE_FILE
}

switch_to_monochrome() {
	case "$vendor" in
		ingenic)
			/usr/sbin/imp-control.sh ispmode 1
			;;
		*)
			curl http://127.0.0.1/night/on
			;;
	esac
	echo "Switched to monochrome mode"
	echo "night" >$MODE_FILE
}

case "$1" in
	off)
		switch_to_monochrome
		;;
	on)
		switch_to_color
		;;
	~ | toggle)
		if [ "$(cat $MODE_FILE 2>/dev/null)" = "day" ]; then
			switch_to_monochrome
		else
			switch_to_color
		fi
		;;
	*)
		echo "Unknown mode"
		exit 1
		;;
esac

exit 0