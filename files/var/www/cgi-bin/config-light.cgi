#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Illumination"
if [ "POST" = "$REQUEST_METHOD" ]; then
	error=""

	if [ -n "$POST_day_night_limit" ]; then
		if [ -n "$POST_day_night_tolerance" ]; then
			day_night_max=$(( $POST_day_night_limit + $POST_day_night_tolerance ))
			day_night_min=$(( $POST_day_night_limit - $POST_day_night_tolerance ))
		fi
	fi

	[ -z "$day_night_min" ] && day_night_min=400
	[ -z "$day_night_max" ] && day_night_max=600

	update_uboot_env ir850_led_pin $POST_ir850_led_pin
	update_uboot_env ir940_led_pin $POST_ir940_led_pin
	update_uboot_env white_led_pin $POST_white_led_pin
	update_uboot_env day_night_min $day_night_min
	update_uboot_env day_night_max $day_night_max

	# save 850 mn pin into Majestic config
	cli -s .nightMode.backlightPin $POST_ir850_led_pin
fi

ir850_led_pin=$(fw_printenv -n ir850_led_pin)
ir940_led_pin=$(fw_printenv -n ir940_led_pin)
white_led_pin=$(fw_printenv -n white_led_pin)
day_night_min=$(fw_printenv -n day_night_min)
day_night_max=$(fw_printenv -n day_night_max)

if [ -n "$day_night_min" ]; then
	if [ -n "$day_night_max" ]; then
		day_night_tolerance=$(( ($day_night_max - $day_night_min) / 2 ))
		day_night_limit=$(( $day_night_min + $day_night_tolerance ))
	fi
fi

[ -z "$day_night_limit" ] && day_night_limit=500
[ -z "$day_night_tolerance" ] && day_night_tolerance=100
%>
<%in p/header.cgi %>

<form action="<%= $SCRIPT_NAME %>" method="post">
  <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
    <div class="col">
      <% field_number "ir850_led_pin" "850 nm IR LED GPIO pin" %>
      <% field_number "ir940_led_pin" "940 nm IR LED GPIO pin" %>
      <% field_number "white_led_pin" "White Light LED GPIO pin" %>
      <% field_number "day_night_limit" "Day/Night Trigger Level" %>
      <% field_number "day_night_tolerance" "Day/Night Tolerance" %>
    </div>
    <div class="col">
      <h3>Environment settings</h3>
      <pre>
ir850_led_pin: <%= $ir850_led_pin %>
ir940_led_pin: <%= $ir940_led_pin %>
white_led_pin: <%= $white_led_pin %>
day_night_min: <%= $day_night_min %>
day_night_max: <%= $day_night_max %>
</pre>
    </div>
    <div class="col">
      <% button_webui_log %>
    </div>
  </div>
  <% button_submit %>
</form>

<%in p/footer.cgi %>
