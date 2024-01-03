#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Illumination"
if [ "POST" = "$REQUEST_METHOD" ]; then
	error=""

	if [ -n "$POST_day_night_threshold" ]; then
		if [ -n "$POST_day_night_tolerance" ]; then
			day_night_max=$(( $POST_day_night_threshold + $POST_day_night_tolerance ))
			day_night_min=$(( $POST_day_night_threshold - $POST_day_night_tolerance ))
		fi
	fi

	[ -z "$day_night_min" ] && day_night_min=400
	[ -z "$day_night_max" ] && day_night_max=600

	# save values to env
	update_uboot_env ir850_led_pin $POST_ir850_led_pin
	update_uboot_env ir940_led_pin $POST_ir940_led_pin
	update_uboot_env white_led_pin $POST_white_led_pin
	update_uboot_env day_night_min $day_night_min
	update_uboot_env day_night_max $day_night_max
	update_uboot_env ircut_pins "$POST_ircut_pin1 $POST_ircut_pin2"

	# update Majestic config
	cli -s .nightMode.irCutPin1 $ircut_pin1
	cli -s .nightMode.irCutPin2 $ircut_pin2
	# take the first non-empty LED pin and use as backlight pin in majestic
	backlight_pin=$(echo "$POST_ir850_led_pin $POST_ir940_led_pin $POST_white_led_pin" | awk '{print $1}')
	cli -s .nightMode.backlightPin $backlight_pin
fi

# read data from env
ir850_led_pin=$(fw_printenv -n ir850_led_pin)
ir940_led_pin=$(fw_printenv -n ir940_led_pin)
white_led_pin=$(fw_printenv -n white_led_pin)
day_night_min=$(fw_printenv -n day_night_min)
day_night_max=$(fw_printenv -n day_night_max)
ircut_pins=$(fw_printenv -n ircut_pins)
ircut_pin1=$(echo $ircut_pins | awk '{print $1}')
ircut_pin2=$(echo $ircut_pins | awk '{print $2}')

ircut_pin1=$(echo $ircut_pins | awk '{print $1}')
ircut_pin2=$(echo $ircut_pins | awk '{print $2}')

# reuse Majestic values is not found in env
if [ -z "$ir850_led_pin" ]; then
	ir850_led_pin=$(cli -g .nightMode.backlightPin)
fi

if [ -z "$ircut_pins" ]; then
	ircut_pin1=$(cli -g .nightMode.irCutPin1)
	ircut_pin2=$(cli -g .nightMode.irCutPin2)
	ircut_pins="$ircut_pin1 $ircut_pin2"
fi

# calculate threshold and tolerance from min and max limits
if [ -n "$day_night_min" ]; then
	if [ -n "$day_night_max" ]; then
		day_night_tolerance=$(( ($day_night_max - $day_night_min) / 2 ))
		day_night_threshold=$(( $day_night_min + $day_night_tolerance ))
	fi
fi

[ -z "$day_night_threshold" ] && day_night_threshold=500
[ -z "$day_night_tolerance" ] && day_night_tolerance=100
%>
<%in p/header.cgi %>

<form action="<%= $SCRIPT_NAME %>" method="post">
  <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
    <div class="col">
      <% field_number "ir850_led_pin" "850 nm IR LED GPIO pin" %>
      <% field_number "ir940_led_pin" "940 nm IR LED GPIO pin" %>
      <% field_number "white_led_pin" "White Light LED GPIO pin" %>
      <% field_number "day_night_threshold" "Day/Night Trigger Threshold" %>
      <% field_number "day_night_tolerance" "Day/Night Tolerance" %>
      <% field_number "ircut_pin1" "IR CUT filter GPIO pin 1" %>
      <% field_number "ircut_pin2" "IR CUT filter GPIO pin 2" %>
    </div>
    <div class="col">
      <h3>Environment settings</h3>
      <pre>
ir850_led_pin: <%= $ir850_led_pin %>
ir940_led_pin: <%= $ir940_led_pin %>
white_led_pin: <%= $white_led_pin %>
day_night_min: <%= $day_night_min %>
day_night_max: <%= $day_night_max %>
ircut_pins: <%= $ircut_pins %>
</pre>
    </div>
    <div class="col">
      <% button_webui_log %>
    </div>
  </div>
  <% button_submit %>
</form>

<%in p/footer.cgi %>
