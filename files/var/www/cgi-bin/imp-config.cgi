#!/usr/bin/haserl
<%in p/common.cgi %>
<%
imp_config_file=/etc/webui/imp.cfg
mj_config_file=/etc/majestic.yaml

page_title="IMP Configuration"

commands_unchecked="aiagc aigain aecomp aeitmax again dgain whitebalance sensorfps backlightcomp framerate gopattr
setbitrate setgoplength setqp setqpbounds setqpipdelta rcmode aemin autozoom frontcrop mask"

commands_do_not_work="ains"

commands="aecomp aiaec aialc aigain aihpf aivol aogain aovol
brightness contrast defogstrength dpc drc flicker flip hilight hue ispmode
saturation sharpness sinter temper"

# reading values
for i in $commands; do
	eval "$i=$(/usr/sbin/imp-control.sh $i)"
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
<pre>
<%
for i in $commands; do
	eval "echo $i = \$$i"
done
%>
</pre>
</div>

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
			<% field_range "aecomp" "AE Compensation" "0,255" %>
			<% field_range "dpc" "DPC Strength" "0,255" %>
			<% field_range "drc" "DRC Strength" "0,255" %>
			<% field_range "defogstrength" "Defog Strength" "0,255" %>
			<% field_range "hilight" "Highlight Intensity" "0,10" %>
			<% field_number "aeitmax" "AE Max Parameters" %>
			<% field_number "again" "Analog Gain" %>
			<% field_number "dgain" "Digital Gain" %>
			<% field_number "backlightcomp" "Backlight Compensation Strength" %>
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
<% field_select "encchn" "Encoder Channel" "0,1" %>

<b>White Balance</b>
<% field_number "whitebalance_mode" "Mode" %>
<% field_number "whitebalance_rgain" "R Gain" %>
<% field_number "whitebalance_bgain" "B Gain" %>
<b>Sensor FPS</b>
<% field_number "sensorfps_num" "Number" %>
<% field_number "sensorfps_den" "Density" %>
<b>Sensor Frame Rate</b>
<% field_number "framerate_num" "Number" %>
<% field_number "framerate_den" "Density" %>
<b>Bit Rate</b>
<% field_number "setbitrate_tgtbr" "Target Bitrate" %>
<% field_number "setbitrate_maxbr" "Maximum Bitrate" %>
<b>GOP Attributes</b>
<% field_number "gopattr_length" "GOP Length" %>
<b>GOP Length</b>
<% field_number "setgoplength_length" "GOP Length" %>
<b>QP</b>
<% field_number "setqp_qp" "QP" %>
<% field_number "setqpbounds_minqp" "Minimum QP" %>
<% field_number "setqpbounds_maxqp" "Maximum QP" %>
<% field_number "setqpipdelta_ipdelta" "QP IP Delta" %>
<b>Rate Control Mode</b>
<% field_number "rcmode_mode" "Mode" %>
<% field_text "rcmode_params" "Parameters" %>
<b>Set AE Min Parameters</b>
<% field_number "aemin_min_it" "Minimum IT" %>
<% field_number "aemin_min_again" "Minimum aGain" %>
<% field_number "aemin_min_it_short" "Minimum IT Short" %>
<% field_number "aemin_min_again_short" "Minimum aGain Short" %>

<b>Set Auto Zoom</b>
<% field_number "autozoom_ch" "Channel" %>
<% field_number "autozoom_sc_en" "Scaler Enabled" %>
<% field_number "autozoom_sc_w" "Scale Width" %>
<% field_number "autozoom_sc_w" "Scale Height" %>
<% field_number "autozoom_cr_en" "Crop Enabled" %>
<% field_number "autozoom_cr_l" "Crop Left" %>
<% field_number "autozoom_cr_t" "Crop Top" %>
<% field_number "autozoom_cr_w" "Crop Width" %>
<% field_number "autozoom_cr_h" "Crop Height" %>

<b>Set Front Crop</b>
<% field_number "frontcrop_en" "Crop Enable" %>
<% field_number "frontcrop_t" "Crop Top" %>
<% field_number "frontcrop_l" "Crop Left" %>
<% field_number "frontcrop_w" "Crop Width" %>
<% field_number "frontcrop_h" "Crop Height" %>

<b>Set Mask</b>
<% field_number "mask_en" "Mask Enable" %>
<% field_number "mask_t" "Mask Top" %>
<% field_number "mask_l" "Mask Left" %>
<% field_number "mask_w" "Mask Width" %>
<% field_number "mask_h" "Mask Height" %>
<% field_number "mask_g" "Mask Green" %>
<% field_number "mask_b" "Mask Blue" %>
<% field_number "mask_r" "Mask Red" %>

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