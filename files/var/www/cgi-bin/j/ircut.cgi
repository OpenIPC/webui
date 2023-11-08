#!/bin/sh

export_pin() {
	[ ! -d "/sys/class/gpio/gpio${1}" ] && echo $1 > /sys/class/gpio/export
}

unexport_pin() {
	[ -d "/sys/class/gpio/gpio${1}" ] && echo $1 > /sys/class/gpio/unexport
}

set_pin_output() {
	echo out > /sys/class/gpio/gpio${1}/direction
}

set_pin_active_low() {
	echo 0 > /sys/class/gpio/gpio${1}/active_low
}

set_pin_value() {
	echo $2 > /sys/class/gpio/gpio${1}/value
}

get_pin_value() {
	cat /sys/class/gpio/gpio${1}/value
}

deactivate_pin() {
	echo 0 > /sys/class/gpio/gpio${1}/value
	usleep 10000
	echo $2 > /sys/class/gpio/gpio${1}/value
}

initialize_pins() {
	for pin in $PIN1 $PIN2; do
		export_pin $pin
		set_pin_output $pin
		set_pin_active_low $pin
	done
}

toggle_ircut() {
	set_pin_value $PIN1 0
	usleep 10000
	set_pin_value $PIN1 $1
	set_pin_value $PIN2 $2
	usleep 10000
	set_pin_value $PIN1 0
	set_pin_value $PIN2 0
}

# read IRCUT pins from bootloader environment
PIN1=$(fw_printenv -n ircut_pin1)
PIN2=$(fw_printenv -n ircut_pin2)

# read IRCUT pins from majestic config, if empty
[ -z "$PIN1" ] && PIN1=$(cli -g .nightMode.irCutPin1)
[ -z "$PIN2" ] && PIN2=$(cli -g .nightMode.irCutPin2)

if [ -z "$PIN1" ] || [ -z "$PIN2" ]; then
	echo "Please define IR-CUT pins:"
	echo "fw_setenv ircut_pin1 <pin>"
	echo "fw_setenv ircut_pin2 <pin>"
	exit 1
fi

# parse parameters from query string
eval $(echo ${QUERY_STRING//&/;})

case "$mode" in
"on")
	pin1value=0
	pin2value=1
	initialize_pins
	toggle_ircut $pin1value $pin2value
	;;
"off")
	pin1value=1
	pin2value=0
	initialize_pins
	toggle_ircut $pin1value $pin2value
	;;
*)
	pin1value=$(get_pin_value "$PIN1")
	pin2value=$(get_pin_value "$PIN2")
	;;
esac

payload=$(printf '{"ircut":[{"pin1":{"no":"%s","value":"%s"}},{"pin2":{"no":"%s","value":"%s"}}]}' $PIN1 $pin1value $PIN2 $pin2value)
echo "HTTP/1.1 200 OK
Content-type: application/json
Pragma: no-cache
Expires: $(TZ=GMT0 date +'%a, %d %b %Y %T %Z')
Etag: \"$(cat /proc/sys/kernel/random/uuid)\"

${payload}
"
