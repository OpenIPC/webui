#!/bin/sh

plugin="daynight"
source /usr/sbin/common-plugins
singleton

STOP_FILE=/tmp/daynight.stop
SUPPORTED="ingenic sigmastar"

vendor=$(ipcinfo --vendor)
[ -z "$(echo "$SUPPORTED" | sed -n "/\b${vendor}\b/p")" ] &&
	log "Day/night plugin is not supported on your camera!" && exit 1

reversed=0
case "$vendor" in
	"ingenic")
		value=$(cat /proc/jz/isp/isp-m0 | grep 'ISP EV value:' | awk '{print $4}')
		reversed=1
		;;
	"sigmastar")
		# GPIO78, PAD_SAR_GPIO0 -> channel 0
		# GPIO79, PAD_SAR_GPIO1 -> channel 1
		# GPIO80, PAD_SAR_GPIO2 -> channel 2
		# GPIO81, PAD_SAR_GPIO3 -> channel 3
		echo 2 > /sys/devices/virtual/mstar/sar/channel
		value=$(cat /sys/devices/virtual/mstar/sar/value)
		;;
	*)
		echo "vendor is not supported"
		exit 1
		;;
esac

day_night_max=$(fw_printenv -n day_night_max)
day_night_min=$(fw_printenv -n day_night_min)

#                         day_night_limit
#                |<--------------|------------------ day --- 1024
#                |            hysteresis         |
# 0 --- night -----------------------------------|
#                |-- tolerance --|-- tolerance --|

if [ "$reversed" -gt "0" ]; then
	if [ "$value" -lt "$day_night_min" ]; then
		echo "$value < $day_night_min Switch to DAY"
		curl -s http://127.0.0.1/night/off
	elif [ "$value" -gt "$day_night_max" ]; then
		echo "$value > $day_night_max Switch to NIGHT"
		curl -s http://127.0.0.1/night/on
	fi
else
	if [ "$value" -gt "$day_night_max" ]; then
		echo "$value > $day_night_max Switch to DAY"
		curl -s http://127.0.0.1/night/off
	elif [ "$value" -lt "$day_night_min" ]; then
		echo "value < $day_night_min Switch to NIGHT"
		curl -s http://127.0.0.1/night/on
	fi
fi

exit 0