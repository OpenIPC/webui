#!/bin/sh

# set parameters from cli, if empty
[ -z "$mode" ] && mode=$1
[ -z "$type" ] && type=$2

# set parameters to default values, if empty
[ -z "$type" ] && type="ir850" # most common IR led

# read LED pin from bootloader environment
pin=$(fw_printenv -n ${type}_led_pin)

if [ -z "$pin" ]; then
	# read LED pin from majestic config
	case "$type" in
		ir850)
			[ -z "$pin" ] && pin=$(cli -g .nightMode.backlightPin)
			;;
		ir940)
			#[ -z "$pin" ] && pin=$(cli -g .nightMode.backlightPin)
			;;
		white)
			#[ -z "$pin" ] && pin=$(cli -g .nightMode.backlightPin)
			;;
		*)
			echo "Unknown LED type"
			exit 2
			;;
	esac
fi

if [ -z "$pin" ]; then
	echo "Please define ${type} GPIO pin"
	echo "fw_setenv ${type}_led_pin <pin>"
	exit 1
fi

case "$mode" in
	on | 1)
		gpio set $pin >/dev/null
		;;
	off | 0)
		gpio clear $pin >/dev/null
		;;
  	~ | toggle)
   		gpio toggle $pin >/dev/null
     		;;
	*)
		echo "Unknown mode"
		exit 3
		;;
esac

exit 0
