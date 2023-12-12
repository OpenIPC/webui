#!/usr/bin/haserl
<%in p/common.cgi %>
<%in p/icons.cgi %>
<%
imp_config_file=/etc/imp.conf
imp_config_temp_file=/tmp/imp.conf
mj_config_file=/etc/majestic.yaml

if [ "POST" = "$REQUEST_METHOD" ]; then
	# save changes to IMP config file
	if [ -n "$POST_save_changes" ] && [ -f "$imp_config_temp_file" ]; then
		sort $imp_config_temp_file > $imp_config_file
	fi

	# reset changes and start afresh
	if [ -n "$POST_reset_changes" ]; then
		[ -f "$imp_config_file" ] && rm $imp_config_file
		[ -f "$imp_config_temp_file" ] && rm $imp_config_temp_file
		/etc/init.d/S95majestic restart >/dev/null
		sleep 1
	fi

	# reload the page via GET to allow clean refresh
	redirect_to $SCRIPT_NAME
fi

page_title="IMP Configuration"

commands_do_not_work="aemin aiaec aiagc aihpf ains aogain aovol autozoom
framerate gopattr mask rcmode setbitrate setgoplength setqp
setqpbounds setqpipdelta whitebalance"

commands="aecomp aeitmax again aigain aialc aigain aivol backlightcomp brightness
contrast defogstrength dgain dpc drc flicker flip frontcrop hilight hue ispmode
saturation sensorfps setosdalpha setosdpos sharpness sinter temper"

commands_channel="framerate"

# create a copy of IMP config file
cp -f $imp_config_file $imp_config_temp_file

# reading actual values from implib
for i in $commands; do
	eval "$i=\"$(/usr/sbin/imp-control.sh $i)\""
done

# read values from temp config file
# if grep -q "^$i\s" $imp_config_temp_file; then
#	eval "$i=\"$(sed -n "/^$i\s/p" $imp_config_temp_file | cut -d" " -f2-)\""
# fi

# convert complex values
if [ -n "$setosdpos" ]; then
	setosdpos_x=$(echo "$setosdpos" | awk '{print $2}')
	setosdpos_y=$(echo "$setosdpos" | awk '{print $3}')
fi

if [ -n "$whitebalance" ]; then
	whitebalance_mode=$(echo "$whitebalance" | awk '{print $1}')
	whitebalance_rgain=$(echo "$whitebalance" | awk '{print $2}')
	whitebalance_bgain=$(echo "$whitebalance" | awk '{print $3}')
fi

# normalize values
[ "$aiaec" = "on" ] && aiaec="true"
[ "$aihpf" = "on" ] && aihpf="true"
[ -z "$setosdpos_x" ] && setosdpos_x=0
[ -z "$setosdpos_y" ] && setosdpos_y=0

check_flip() {
	[ $flip -eq 2 ] || [ $flip -eq 3 ] && echo -n " checked"
}

check_mirror() {
	[ $flip -eq 1 ] || [ $flip -eq 3 ] && echo -n " checked"
}
%>
<%in p/header.cgi %>

<div class="row row-cols-4 g-4">
  <div class="col">
    <div class="card mb-3">
      <h5 class="card-header">Video Output</h5>
      <div class="card-body">
        <%# field_switch "ispmode" "$icon_moon" %>
        <div class="row">
          <div class="col mb-3">
            <p class="form-label">Color</p>
            <div class="btn-group d-flex" role="group" aria-label="Night Mode">
              <input type="radio" class="btn-check" name="ispmode" id="ispmode_day" value="0"<% checked_if $ispmode 0 %>>
              <label class="btn btn-outline-primary" for="ispmode_day" title="Day mode"><%= $icon_sun %></label>
              <input type="radio" class="btn-check" name="ispmode" id="ispmode_night" value="1"<% checked_if $ispmode 1 %>>
              <label class="btn btn-outline-primary" for="ispmode_night" title="Night mode"><%= $icon_moon %></label>
            </div>
          </div>
          <div class="col mb-3">
            <p class="form-label">Flip</p>
            <div class="btn-group d-flex" role="group" aria-label="Flip and Mirror">
              <input type="checkbox" class="btn-check" name="flip" id="flip" value="1"<% check_flip %>>
              <label class="btn btn-outline-primary" for="flip" title="Flip vertically"><%= $icon_flip %></label>
              <input type="checkbox" class="btn-check" name="mirror" id="mirror" value="1"<% check_mirror %>>
              <label class="btn btn-outline-primary" for="mirror" title="Flip horizontally"><%= $icon_flop %></label>
            </div>
          </div>
        </div>
        <div class="mb-3">
          <p class="form-label">Anti-Flicker</p>
          <div class="btn-group d-flex" role="group" aria-label="Anti-flicker">
            <input type="radio" class="btn-check" name="flicker" id="flicker_off" value="0"<% checked_if "$flicker" 0 %>>
            <label class="btn btn-outline-primary" for="flicker_off">OFF</label>
            <input type="radio" class="btn-check" name="flicker" id="flicker_50" value="1"<% checked_if "$flicker" 1 %>>
            <label class="btn btn-outline-primary" for="flicker_50">50 Hz</label>
            <input type="radio" class="btn-check" name="flicker" id="flicker_60" value="2"<% checked_if "$flicker" 2 %>>
            <label class="btn btn-outline-primary" for="flicker_60">60 Hz</label>
          </div>
        </div>
        <% field_range "sensorfps" "Sensor FPS" "5,30" %>
        <% field_range "brightness" "Brightness" "0,255" %>
        <% field_range "contrast" "Contrast" "0,255" %>
        <% field_range "saturation" "Saturation" "0,255" %>
        <% field_range "hue" "Hue" "0,255" %>
        <% field_range "sharpness" "Sharpness" "0,255" %>
        <% field_range "sinter" "Sinter Strength" "0,255" %>
        <% field_range "temper" "Temper Strength" "0,255" %>
      </div>
    </div>
  </div>
  <div class="col">
    <div class="card mb-3">
      <h5 class="card-header">Video Output</h5>
      <div class="card-body">
        <% field_range "aecomp" "AE Compensation" "0,255" %>
        <% field_range "dpc" "DPC Strength" "0,255" %>
        <% field_range "drc" "DRC Strength" "0,255" %>
        <% field_range "defogstrength" "Defog Strength" "0,255" %>
        <% field_range "hilight" "Highlight Intensity" "0,10" %>
        <% field_number "aeitmax" "AE Max Parameters" %>
        <% field_number "again" "Analog Gain" %>
        <% field_number "dgain" "Digital Gain" %>
        <% field_number "backlightcomp" "Backlight Compensation" %>
        <div class="row">
          <div class="col">
            <% field_number "whitebalance_mode" "Mode" %>
          </div>
          <div class="col">
            <% field_number "whitebalance_rgain" "RGain" %>
          </div>
          <div class="col">
            <% field_number "whitebalance_bgain" "BGain" %>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="col">
    <div class="card mb-3">
      <h5 class="card-header">Audio Input</h5>
      <div class="card-body">
        <% field_range "aivol" "Audio Input Volume" "-30,120" %>
        <% field_range "aigain" "Audio Input Gain" "0,31" %>
        <%# field_select "aiagc" "Auto Gain Control" "off,gainLevel compGaindB" %>
        <% field_range "aialc" "Audio Input ALC Gain" "0,7" %>
        <% field_switch "aihpf" "High Pass Filter" %>
        <% field_switch "aiaec" "Echo Cancellation" %>
        <%# field_range "ains" "Noise Suppression" "-1,3" %>
      </div>
    </div>
    <div class="card mb-3">
      <h5 class="card-header">Audio Output</h5>
      <div class="card-body">
        <% field_range "aovol" "Audio Output Volume", "-30,120" %>
        <% field_range "aogain" "Audio Output Gain" "0,31" %>
      </div>
    </div>
  </div>
  <div class="col">
    <div class="card mb-3">
      <h5 class="card-header">OSD</h5>
      <div class="card-body">
        <% field_range "setosdalpha" "Opacity" "0,255" %>
        <div class="row">
          <div class="col">
            <% field_number "setosdpos_x" "X-position" %>
          </div>
          <div class="col">
            <% field_number "setosdpos_y" "Y-position" %>
          </div>
        </div>
      </div>
    </div>

    <% field_text "frontcrop" "Front Crop" %>
  </div>
</div>

<div id="savechanges" class="alert alert-warning mb-3 d-none">
  <p class="mb-0">Please do not forget to save your changes!</p>
</div>

<div class="row">
  <div class="col-auto me-auto mb-3">
    <form action="<%= $SCRIPT_NAME %>" method="post" class="mb-3">
      <input type="hidden" name="save_changes" value="1">
      <input type="submit" value="Save Changes" class="btn btn-primary">
    </form>
  </div>
  <div class="col-auto mb-3">
    <form action="<%= $SCRIPT_NAME %>" method="post" class="mb-3">
      <input type="hidden" name="reset_changes" value="1">
      <input type="submit" value="Reset to default" class="btn btn-danger">
    </form>
  </div>
</div>

<h3>Debug</h3>
<div class="row">
  <div class="col col-3 mb-3">
    <b>/etc/imp.conf</b>
    <pre><% cat /etc/imp.conf %></pre>
    <b>/tmp/imp.conf</b>
    <pre><% cat /tmp/imp.conf %></pre>
  </div>
  <div class="col col-3 mb-3">
    <b>in memory values</b>
    <pre><% for i in $commands; do eval "echo $i = \$$i"; done %></pre>
  </div>
  <div class="col col-6 mb-3">
    <b>commands to fix</b>
    <pre><% for i in $commands_do_not_work; do echo -e "$i\n$(/usr/sbin/imp-control.sh $i)\n"; done %></pre>
  </div>
</div>

<script src="/a/imp-config.js"></script>

<%in p/footer.cgi %>