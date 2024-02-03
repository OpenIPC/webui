#!/bin/sh

# set parameters from cli, if empty
[ -z "$mode" ] && mode=$1

MODE_FILE=/tmp/colormode.txt

switch_to_color() {
	curl http://127.0.0.1/night/off
	echo "Switched to full-color mode"
	echo "day" >$MODE_FILE
}

switch_to_monochrome() {
	curl http://127.0.0.1/night/on
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
