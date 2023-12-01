#!/bin/sh

# set parameters from cli, if empty
[ -z "$mode" ] && mode=$1
[ -z "$type" ] && type=$2

# set parameters to default values, if empty
[ -z "$type" ] && type="ir850" # most common IR led

# read LED pin from bootloader environment
PIN=$(fw_printenv -n ${type}_led_pin)

if [ -z "$PIN" ]; then
	# read LED pin from majestic config
	case "$type" in
	"ir850")
		[ -z "$PIN" ] && PIN=$(cli -g .nightMode.backlightPin)
		;;
	"ir940")
		#[ -z "$PIN" ] && PIN=$(cli -g .nightMode.backlightPin)
		;;
	"white")
		#[ -z "$PIN" ] && PIN=$(cli -g .nightMode.backlightPin)
		;;
	esac
fi

if [ -z "$PIN" ]; then
	echo "Please define ${type} GPIO pin"
	echo "fw_setenv ${type}_led_pin <pin>"
	exit 1
fi

case "$mode" in
	"on"|"1")
		gpio set $PIN >/dev/null
		;;
	"off"|"0")
		gpio clear $PIN >/dev/null
		;;
	*)
		;;
esac

exit 0