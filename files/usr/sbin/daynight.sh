#!/bin/sh

plugin="daynight"

. /usr/sbin/common-plugins
singleton

STOP_FILE=/tmp/daynight.stop
MODE_FILE=/tmp/nightmode.txt

vendor=$(ipcinfo --vendor)

switch_to_day() {
	/usr/sbin/color.sh on
	/usr/sbin/irled.sh off
	/usr/sbin/ircut.sh on
}

switch_to_night() {
	/usr/sbin/color.sh off
	/usr/sbin/irled.sh on
	/usr/sbin/ircut.sh off
}

# determine luminance of the scene
reversed=0
case "$vendor" in
	ingenic)
		value=$(awk '/ISP EV value:/ {print $4}' /proc/jz/isp/isp-m0)
		reversed=1
		;;
	sigmastar)
		# GPIO78, PAD_SAR_GPIO0 -> channel 0
		# GPIO79, PAD_SAR_GPIO1 -> channel 1
		# GPIO80, PAD_SAR_GPIO2 -> channel 2
		# GPIO81, PAD_SAR_GPIO3 -> channel 3
		echo 2 >/sys/devices/virtual/mstar/sar/channel
		value=$(cat /sys/devices/virtual/mstar/sar/value)
		;;
	*)
		echo "vendor is not supported"
		exit 1
		;;
esac

case "$1" in
	night)
		switch_to_night
		;;
	day)
		switch_to_day
		;;
	toggle)
		case "$vendor" in
			ingenic)
#				if [ "Day" = "$(awk '/ISP Runing Mode/ {print $5}' /proc/jz/isp/isp-m0)" ]; then
				if [ "$(/usr/sbin/imp-control.sh ispmode)" -eq 0 ]; then
					switch_to_night
				else
					switch_to_day
				fi
				;;
			*)
				if [ "day" = "$(cat $MODE_FILE 2>/dev/null)" ]; then
					switch_to_night
				else
					switch_to_day
				fi
				;;
		esac
		;;
	*)
		day_night_max=$(fw_printenv -n day_night_max)
		day_night_min=$(fw_printenv -n day_night_min)

		echo "$day_night_min - $value - $day_night_max"

		if [ "$reversed" -eq 0 ]; then
			if [ "$value" -lt "$day_night_min" ]; then
				switch_to_day
			elif [ "$value" -gt "$day_night_max" ]; then
				switch_to_night
			fi
		else
			if [ "$value" -gt "$day_night_max" ]; then
				switch_to_night
			elif [ "$value" -lt "$day_night_min" ]; then
				switch_to_day
			fi
		fi
		;;
esac

exit 0
