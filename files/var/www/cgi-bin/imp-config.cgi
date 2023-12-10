#!/usr/bin/haserl
<%in p/common.cgi %>
<%
imp_config_file=/etc/imp.conf
imp_config_temp_file=/tmp/imp.conf
mj_config_file=/etc/majestic.yaml

if [ "POST" = "$REQUEST_METHOD" ]; then
	# save changes to IMP config file
	if [ -n "$POST_save_changes" ] && [ -f "$imp_config_temp_file" ]; then
		sort $imp_config_temp_file > $imp_config_file
	fi
	# reopen via GET to allow clean refresh
	redirect_to $SCRIPT_NAME
fi


page_title="IMP Configuration"

commands_do_not_work="ains framerate frontcrop mask rcmode setbitrate
setgoplength setqp setqpbounds setqpipdelta"

commands="aecomp aeitmax aemin again aiaec aigain aiagc aialc aigain aihpf
aivol aogain aovol autozoom backlightcomp brightness contrast defogstrength
dgain dpc drc flicker flip gopattr hilight hue ispmode saturation sensorfps
sharpness sinter temper whitebalance"

commands_channel="framerate"

# create a copy of IMP config file
cp -f $imp_config_file $imp_config_temp_file

# reading values
for i in $commands; do
	if grep -q "^$i\s" $imp_config_temp_file; then
		eval "$i=$(awk "/^$i\s/ {print \$2}" $imp_config_temp_file)"
	else
		eval "$i=$(/usr/sbin/imp-control.sh $i)"
	fi
	#while read -r line; do /usr/sbin/imp-control.sh $line; done < /etc/imp.conf
done

# normalizing values
[ "$ispmode" -eq 1 ] && ispmode="true"
[ "$aihpf" = "on" ] && aihpf=1

check_flip() {
	[ $flip -eq 2 ] || [ $flip -eq 3 ] && echo " checked"
}

check_mirror() {
	[ $flip -eq 1 ] || [ $flip -eq 3 ] && echo " checked"
}
%>
<%in p/header.cgi %>

<div class="row row-cols-4 g-4">
  <div class="col">
    <div class="card mb-3">
      <h5 class="card-header">Video Output</h5>
      <div class="card-body">
        <% field_switch "ispmode" "Night Mode" %>
        <div class="mb-3">
          <p class="form-label">Anti-Flicker</p>
          <div class="btn-group" role="group" aria-label="Anti-flicker">
            <input type="radio" class="btn-check" name="flicker" id="flicker_off" value="0"<% [ "$flicker" -eq 0 ] && echo " checked" %>>
            <label class="btn btn-outline-primary" for="flicker_off">OFF</label>
            <input type="radio" class="btn-check" name="flicker" id="flicker_50" value="1"<% [ "$flicker" -eq 1 ] && echo " checked" %>>
            <label class="btn btn-outline-primary" for="flicker_50">50 Hz</label>
            <input type="radio" class="btn-check" name="flicker" id="flicker_60" value="2"<% [ "$flicker" -eq 2 ] && echo " checked" %>>
            <label class="btn btn-outline-primary" for="flicker_60">60 Hz</label>
          </div>
        </div>
        <div class="mb-3">
          <p class="form-label">Image Transformation</p>
          <div class="btn-group" role="group" aria-label="Anti-flicker">
            <input type="checkbox" class="btn-check" name="flip" id="flip" value="1"<% check_flip %>>
            <label class="btn btn-outline-primary" for="flip">Flip</label>
            <input type="checkbox" class="btn-check" name="mirror" id="mirror" value="1"<% check_mirror %>>
            <label class="btn btn-outline-primary" for="mirror">Mirror</label>
          </div>
        </div>
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
        <% field_number "backlightcomp" "Backlight Compensation Strength" %>
        <% field_number "sensorfps" "Sensor FPS" %>
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
</div>

<form action="<%= $SCRIPT_NAME %>" method="post" class="mb-3">
  <input type="hidden" name="save_changes" value="1">
  <input type="submit" value="Save Changes" class="btn btn-primary">
</form>

<h3>Debug</h3>
<div class="row row-cols-2 g-3">
  <div class="col mb-3">
    <b>/etc/imp.conf</b>
    <pre><% cat /etc/imp.conf %></pre>
  </div>
  <div class="col mb-3">
    <b>in memory values</b>
    <pre><% for i in $commands; do eval "echo $i = \$$i"; done %></pre>
  </div>
</div>

<script>
function callImp(command, value) {
	if (["flip", "mirror"].includes(command)) {
		command = "flip"
		value = 0
		if (document.querySelector('#flip').checked) value = (1 << 1)
		if (document.querySelector('#mirror').checked) value += 1
	} else if (["aiaec", "aihpf"].includes(command)) {
		value = (value == 1) ? "on" : "off"
	} else if (["ains"].includes(command)) {
		if (value == -1) value = "off"
	}

	const xhr = new XMLHttpRequest();
	xhr.open('GET', '/cgi-bin/j/imp.cgi?cmd=' + command + '&val=' + value);
	xhr.send();
}

// checkboxes
document.querySelectorAll('input[type=checkbox]').forEach(el => {
	el.autocomplete = "off"
	el.addEventListener('change', ev => callImp(ev.target.name, ev.target.checked ? 1 : 0))
});

// checkboxes
document.querySelectorAll('input[type=radio]').forEach(el => {
	el.autocomplete = "off"
	el.addEventListener('change', ev => callImp(ev.target.name, ev.target.value))
});

// ranges
document.querySelectorAll('input[type=range]').forEach(el => {
	el.addEventListener('change', ev => callImp(ev.target.id.replace('-range', ''), ev.target.value))
});

// selects
document.querySelectorAll('select').forEach(el => {
	el.addEventListener('change', ev => callImp(ev.target.id, ev.target.value))
});
</script>

<%in p/footer.cgi %>