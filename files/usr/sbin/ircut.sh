#!/bin/sh

# set parameters from cli
mode=$1
pin1=$2
pin2=$3

# read IRCUT pins from bootloader environment
ircut_pins=$(fw_printenv -n ircut_pins)
[ -z "$pin1" ] && pin1=$(echo $ircut_pins | awk '{print $1}')
[ -z "$pin2" ] && pin2=$(echo $ircut_pins | awk '{print $2}')

# read IRCUT pins from majestic config, if empty
[ -z "$pin1" ] && pin1=$(cli -g .nightMode.irCutPin1)
[ -z "$pin2" ] && pin2=$(cli -g .nightMode.irCutPin2)

if [ -z "$pin1" ]; then
	echo "Please define IRCUT pin"
	echo "fw_setenv ircut_pins <pin>"
	exit 1
fi

if [ -z "$pin2" ]; then
	echo "Unless you have a single GPIO IRCUT driver, please define the second pin:"
	echo "fw_setenv ircut_pins <pin1> <pin2>"
fi

MODE_FILE=/tmp/ircutmode.txt

vendor=$(ipcinfo --vendor)

ir_filter_off() {
	if [ -z "$pin2" ]; then
		gpio set "$pin1"
	else
		gpio set "$pin1"
		gpio clear "$pin2"
		usleep 10000
		gpio clear "$pin1"
	fi
	echo "IRCUT filter removed"
}

ir_filter_on() {
	if [ -z "$pin2" ]; then
		gpio clear "$pin1"
	else
		gpio clear "$pin1"
		gpio set "$pin2"
		usleep 10000
		gpio clear "$pin2"
	fi
	echo "IRCUT filter set"
}

case "$mode" in
	0 | off | night)
		ir_filter_off
		echo 0 >$MODE_FILE
		;;
	1 | on | day)
		ir_filter_on
		echo 1 >$MODE_FILE
		;;
	~ | toggle)
		if [ "$(cat $MODE_FILE 2>/dev/null)" -eq 0 ]; then
			ir_filter_on
			echo 1 >$MODE_FILE
		else
			ir_filter_off
			echo 0 >$MODE_FILE
		fi
		;;
	*)
		echo "Unknown mode ${mode}"
		exit 1
		;;
esac

exit 0