#!/usr/bin/haserl
<%
IFS_ORIG=$IFS

STR_NOT_SUPPORTED="not supported on this system"

# tag "tag" "text" "css" "extras"
tag() {
	local t="$1"
	local n="$2"
	local c="$3"
	[ -n "$c" ] && c=" class=\"${c}\""
	local x="$4"
	[ -n "$x" ] && x=" ${x}"
	echo "<${t}${c}${x}>${n}</${t}>"
}

# A "tag" "classes" "extras"
A() {
	local c="$2"
	[ -n "$c" ] && c=" class=\"${c}\""
	local x="$3"
	[ -n "$x" ] && x=" ${x}"
	echo "<${1}${c}${x}>"
}

Z() {
	echo "</${1}>"
}

# tag "text" "classes" "extras"
div() {
	tag "div" "$1" "$2" "$3"
}
h1() {
	tag "h1" "$1" "$2" "$3"
}
h2() {
	tag "h2" "$1" "$2" "$3"
}
h3() {
	tag "h3" "$1" "$2" "$3"
}
h4() {
	tag "h4" "$1" "$2" "$3"
}
h5() {
	tag "h5" "$1" "$2" "$3"
}
h6() {
	tag "h6" "$1" "$2" "$3"
}
label() {
	tag "label" "$1" "$2" "$3"
}
li() {
	tag "li" "$1" "$2" "$3"
}
p() {
	tag "p" "$1" "$2" "$3"
}
span() {
	tag "span" "$1" "$2" "$3"
}

div_() {
	A "div" "$1" "$2"
}
_div() {
	Z "div"
}

span_() {
	A "span" "$1" "$2"
}
_span() {
	Z "span"
}

# alert "text" "type" "extras"
alert() {
	echo "<div class=\"alert alert-${2}\" ${3}>${1}</div>"
}

# time_gmt "format" "date"
time_gmt() {
	if [ -n "$2" ]; then
		TZ=GMT0 date +"$1" --date="${2}"
	else
		TZ=GMT0 date +"$1"
	fi
}

time_epoch() {
	time_gmt "%s" "$1"
}

time_http() {
	time_gmt "%a, %d %b %Y %T %Z" "$1"
}

button_download() {
	echo "<a href=\"dl2.cgi?log=${1}\" class=\"btn btn-primary\">Download log</a>"
}

button_mj_backup() {
	echo "<form action=\"majestic-config-actions.cgi\" method=\"post\"><input type=\"hidden\" name=\"action\" value=\"backup\">"
	button_submit "Backup settings"
	echo "</form>"
}

button_mj_reset() {
	echo "<form action=\"majestic-config-actions.cgi\" method=\"post\"><input type=\"hidden\" name=\"action\" value=\"reset\">"
	button_submit "Reset Majestic" "danger"
	echo "</form>"
}

button_reboot() {
	echo "<form action=\"reboot.cgi\" method=\"post\"><input type=\"hidden\" name=\"action\" value=\"reboot\">"
	button_submit "Reboot camera" "danger"
	echo "</form>"
}

button_refresh() {
	echo "<a href=\"${REQUEST_URI}\" class=\"btn btn-primary refresh\">Refresh</a>"
}

button_reset_firmware() {
	echo "<form action=\"firmware-reset.cgi\" method=\"post\"><input type=\"hidden\" name=\"action\" value=\"reset\">"
	button_submit "Reset firmware" "danger"
	echo "</form>"
}

button_restore_from_rom() {
	local file=$1
	[ ! -f "/rom/${file}" ] && return
	if [ -z "$(diff "/rom/${file}" "${file}")" ]; then
		echo "<p class=\"small fst-italic\">File matches the version in ROM.</p>"
		return
	fi
	echo "<p><a class=\"btn btn-danger\" href=\"restore.cgi?f=${file}\">Replace ${file} with its version from ROM</a></p>"
}

# button_submit "text" "type" "extras"
button_submit() {
	local t="$1"
	[ -z "$t" ] && t="Save changes"
	local c="$2"
	[ -z "$c" ] && c="primary"
	local x="$3"
	[ -z "$x" ] && x=" ${x}"
	echo "<div class=\"mt-2\"><input type=\"submit\" class=\"btn btn-${c}\"${x} value=\"${t}\"></div>"
}

button_webui_log() {
	[ -f "/tmp/webui.log" ] && link_to "Download log file" "dl.cgi?file=/tmp/webui.log"
}

check_file_exist() {
	[ ! -f "$1" ] && redirect_back "danger" "File ${1} not found"
}

check_password() {
	_safepage="/cgi-bin/webui-settings.cgi"
	[ "0${debug}" -ge "1" ] && return
	[ -z "$REQUEST_URI" ] || [ "$REQUEST_URI" = "${_safepage}" ] && return
	if [ ! -f /etc/shadow- ] || [ -z $(grep root /etc/shadow- | cut -d: -f2) ]; then
		redirect_to "${_safepage}" "danger" "You must set your own secure password!"
	fi
}

checked_if() {
	[ "$1" = "$2" ] && echo -n " checked"
}

e() {
	echo -e -n "$1"
}

ex() {
	# NB! $() forks process and stalls output.
	echo "<div class=\"${2}\"><h6># ${1}</h6><pre class=\"small\">"
	eval "$1" | sed "s/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g;s/\"/\&quot;/g"
	echo "</pre></div>"
}

# field_checkbox "name" "label" "hint"
field_checkbox() {
	local l=$2
	[ -z "$l" ] && l="$(t_label "$1")"
	[ -z "$l" ] && l="<span class=\"bg-warning\">${1}</span>"
	local h=$3
	local v=$(t_value "$1")
	[ -z "$v" ] && v="false"
	echo "<p class=\"boolean form-check\">" \
		"<input type=\"hidden\" id=\"${1}-false\" name=\"${1}\" value=\"false\">" \
		"<input type=\"checkbox\" name=\"${1}\" id=\"${1}\" value=\"true\" class=\"form-check-input\"$(checked_if "true" "$v")>" \
		"<label for=\"${1}\" class=\"form-label\">${l}</label>"
	[ -n "$h" ] && echo "<span class=\"hint text-secondary d-block mb-2\">${h}</span>"
	echo "</p>"
}

# field_file "name" "label" "hint"
field_file() {
	local l=$2
	[ -z "$l" ] && l="$(t_label "$1")"
	[ -z "$l" ] && l="<span class=\"bg-warning\">${1}</span>"
	local h=$3
	echo "<p class=\"file\">" \
		"<label for=\"${1}\" class=\"form-label\">${l}</label>" \
		"<input type=\"file\" id=\"${1}\" name=\"${1}\" class=\"form-control\">"
	[ -n "$h" ] && echo "<span class=\"hint text-secondary\">${h}</span>"
	echo "</p>"
}

# field_hidden "name" "value"
field_hidden() {
	# do we need id here? id=\"${1}\". We do for netip password!
	echo "<input type=\"hidden\" name=\"${1}\" id=\"${1}\" value=\"${2}\" class=\"form-hidden\">"
}

# field_number "name" "label" "range" "hint"
field_number() {
	local n=$1
	local l=$2
	[ -z "$l" ] && l="$(t_label "$1")"
	[ -z "$l" ] && l="<span class=\"bg-warning\">${1}</span>"
	local r=$3 # min,max,step,button
	local mn=$(echo "$r" | cut -d, -f1)
	local mx=$(echo "$r" | cut -d, -f2)
	local st=$(echo "$r" | cut -d, -f3)
	local ab=$(echo "$r" | cut -d, -f4)
	local h=$4
	local v=$(t_value "$n")
	local vr=$v
	[ -n "$ab" ] && [ "$ab" = "$v" ] && vr=$(( ( $mn + $mx ) / 2 ))
	echo "<p class=\"number\">" \
		"<label class=\"form-label\" for=\"${n}\">${l}</label>" \
		"<span class=\"input-group\">"
	# NB! no name on checkbox, since we don't want its data submitted
	[ -n "$ab" ] && echo "<label class=\"input-group-text\" for=\"${n}-auto\">${ab}" \
		"<input type=\"checkbox\" class=\"form-check-input auto-value ms-1\" id=\"${n}-auto\" data-for=\"${n}\" data-value=\"${vr}\" $(checked_if "$ab" "$v")>" \
		"</label>"
	echo "<input type=\"number\" id=\"${n}\" name=\"${n}\" class=\"form-control text-end\" value=\"${vr}\" min=\"${mn}\" max=\"${mx}\" step=\"${st}\">" \
		"</span>"
	[ -n "$h" ] && echo "<span class=\"hint text-secondary\">${h}</span>"
	echo "</p>"
}

# field_password "name" "label" "hint"
field_password() {
	local l=$2
	[ -z "$l" ] && l="$(t_label "$1")"
	[ -z "$l" ] && l="<span class=\"bg-warning\">${1}</span>"
	local h=$3
	local v=$(t_value "$1")
	echo "<p class=\"password\" id=\"${1}_wrap\">" \
		"<label for=\"${1}\" class=\"form-label\">${l}</label><span class=\"input-group\">" \
		"<input type=\"password\" id=\"${1}\" name=\"${1}\" class=\"form-control\" value=\"${v}\" placeholder=\"K3wLHaZk3R!\">" \
		"<label class=\"input-group-text\">" \
		"<input type=\"checkbox\" class=\"form-check-input me-1\" data-for=\"${1}\"> show" \
		"</label></span>"
	[ -n "$h" ] && echo "<span class=\"hint text-secondary\">${h}</span>"
	echo "</p>"
}

# field_range "name" "label" "range" "hint"
field_range() {
	local n=$1
	local l=$2
	[ -z "$l" ] && l="$(t_label "$n")"
	[ -z "$l" ] && l="<span class=\"bg-warning\">${n}</span>"
	local r=$3 # min,max,step,button
	local mn=$(echo "$r" | cut -d, -f1)
	local mx=$(echo "$r" | cut -d, -f2)
	local st=$(echo "$r" | cut -d, -f3)
	local ab=$(echo "$r" | cut -d, -f4)
	local h=$4
	local v=$(t_value "$n")
	local vr=$v
	[ -z "$vr" -o "$ab" = "$vr" ] && vr=$(( ( $mn + $mx ) / 2 ))
	echo "<p class=\"range\" id=\"${n}_wrap\">" \
		"<label class=\"form-label\" for=\"${n}\">${l}</label>" \
		"<span class=\"input-group\">"
	# NB! no name on checkbox, since we don't want its data submitted
	[ -n "$ab" ] && echo "<label class=\"input-group-text\" for=\"${n}-auto\">${ab}" \
		"<input type=\"checkbox\" class=\"form-check-input auto-value ms-1\" id=\"${n}-auto\" data-for=\"${n}\" data-value=\"${vr}\" $(checked_if "$ab" "$v")>" \
		"</label>"
	# Input that holds the submitting value.
	echo "<input type=\"hidden\" name=\"${n}\" id=\"${n}\" value=\"${v}\">"
	# NB! no name on range, since we don't want its data submitted
	echo "<input type=\"range\" class=\"form-control form-range\" id=\"${n}-range\" value=\"${vr}\" min=\"${mn}\" max=\"${mx}\" step=\"${st}\">"
	echo "<span class=\"input-group-text show-value\" id=\"${n}-show\">${vr}</span>" \
		"</span>"
	[ -n "$h" ] && echo "<span class=\"hint text-secondary\">${h}</span>"
	echo "</p>"
}

# field_select "name" "label" "options" "hint" "units"
field_select() {
	local l=$2
	[ -z "$l" ] && l="$(t_label "$1")"
	[ -z "$l" ] && l="<span class=\"bg-warning\">${1}</span>"
	local o=$3
	o=${o//,/ }
	local h=$4
	local u=$5
	echo "<p class=\"select\" id=\"${1}_wrap\">" \
		"<label for=\"${1}\" class=\"form-label\">${l}</label>" \
		"<select class=\"form-select\" id=\"${1}\" name=\"${1}\">"
	[ -z "$(t_value "$1")" ] && echo "<option value=\"\">Select from available options</option>"
	for o in $o; do
		v="${o%:*}"
		n="${o#*:}"
		[ "$1" != "mj_isp_sensorConfig" ] && n=${n//_/ }
		echo -n "<option value=\"${v}\""
		[ "$(t_value "$1")" = "$v" ] && echo -n " selected"
		echo ">${n}</option>"
		unset v; unset n
	done
	echo "</select>"
	[ -n "$u" ] && echo "<span class=\"input-group-text\">${u}</span>"
	[ -n "$h" ] && echo "<span class=\"hint text-secondary\">${h}</span>"
	echo "</p>"
}

# field_swith "name" "label" "hint" "options"
field_switch() {
	local l=$2
	[ -z "$l" ] && l="$(t_label "$1")"
	[ -z "$l" ] && l="<span class=\"bg-warning\">$1</span>"
	local v=$(t_value "$1")
	[ -z "$v" ] && v="false"
	local h="$3"
	local o=$4
	[ -z "$o" ] && o="true,false"
	local o1=$(echo "$o" | cut -d, -f1)
	local o2=$(echo "$o" | cut -d, -f2)
	echo "<p class=\"boolean\">" \
		"<span class=\"form-check form-switch\">" \
		"<input type=\"hidden\" id=\"${1}-false\" name=\"${1}\" value=\"${o2}\">" \
		"<input type=\"checkbox\" id=\"${1}\" name=\"${1}\" value=\"${o1}\" role=\"switch\" class=\"form-check-input\"$(checked_if "$o1" "$v")>" \
		"<label for=\"$1\" class=\"form-check-label\">${l}</label>" \
		"</span>"
	[ -n "$h" ] && echo "<span class=\"hint text-secondary\">${h}</span>"
	echo "</p>"
}

# field_text "name" "label" "hint" "placeholder"
field_text() {
	local l=$2
	[ -z "$l" ] && l="$(t_label "$1")"
	[ -z "$l" ] && l="<span class=\"bg-warning\">$1</span>"
	local v="$(t_value "$1")"
	local h="$3"
	local p="$4"
	echo "<p class=\"string\" id=\"${1}_wrap\">" \
		"<label for=\"${1}\" class=\"form-label\">${l}</label>" \
		"<input type=\"text\" id=\"${1}\" name=\"${1}\" class=\"form-control\" value=\"${v}\" placeholder=\"${p}\">"
	[ -n "$h" ] && echo "<span class=\"hint text-secondary\">${h}</span>"
	echo "</p>"
}

# field_textarea "name" "label" "hint"
field_textarea() {
	local l=$2
	[ -z "$l" ] && l="$(t_label "$1")"
	[ -z "$l" ] && l="<span class=\"bg-warning\">$1</span>"
	local v=$(t_value "$1")
	local h=$3
	echo "<p class=\"textarea\" id=\"${1}_wrap\">" \
		"<label for=\"${1}\" class=\"form-label\">${l}</label>" \
		"<textarea id=\"${1}\" name=\"${1}\" class=\"form-control\">${v}</textarea>"
	[ -n "$h" ] && echo "<span class=\"hint text-secondary\">${h}</span>"
	echo "</p>"
}

# field_textedit "name" "file" "label"
field_textedit() {
	local l=$3
	[ -z "$l" ] && l="$(t_label "$1")"
	[ -z "$l" ] && l="<span class=\"bg-warning\">$1</span>"
	local v=$(cat "$2")
	echo "<p class=\"textarea\" id=\"${1}_wrap\">" \
		"<label for=\"${1}\" class=\"form-label\">${l}</label>" \
		"<textarea id=\"${1}\" name=\"${1}\" class=\"form-control\">${v}</textarea>"
	echo "</p>"
}

flash_append() {
	echo "$1:$2" >>"$flash_file"
}

flash_delete() {
	:>"$flash_file"
}

flash_read() {
	[ ! -f "$flash_file" ] && return
	[ -z "$(cat $flash_file)" ] && return
	local c
	local m
	local l
	OIFS="$IFS"
	IFS=$'\n'
	for l in $(cat "$flash_file"); do
		c="$(echo $l | cut -d':' -f1)"
		m="$(echo $l | cut -d':' -f2-)"
		echo "<div class=\"alert alert-${c} alert-dismissible fade show\" role=\"alert\">${m}" \
			"<button type=\"button\" class=\"btn btn-close\" data-bs-dismiss=\"alert\" aria-label=\"Close\"></button>" \
			"</div>"
	done
	IFS=$OIFS
	flash_delete
}

flash_save() {
	echo "${1}:${2}" >$flash_file
}

get_soc_temp() {
	[ "true" = "$soc_has_temp" ] && soc_temp=$(ipcinfo --temp)
}

header_bad_request() {
	echo "HTTP/1.1 400 Bad Request
Cache-Control: no-store
Pragma: no-cache
Date: $(time_http)
Server: $SERVER_SOFTWARE

"
}

header_ok() {
	echo "HTTP/1.1 200 OK
Content-type: application/json; charset=UTF-8
Cache-Control: no-store
Pragma: no-cache
Date: $(time_http)
Server: $SERVER_SOFTWARE

{}"
}

html_title() {
	[ -n "$page_title" ] && echo -n "$page_title"
	[ -n "$title" ] && echo -n ": $title"
	echo -n " - OpenIPC"
}

# label "name" "classes" "extras" "units"
label() {
	local c="form-label"
	[ -n "$2" ] && c="${c} ${2}"
	local l="$(t_label "$1")"
	[ -z "$l" ] && l="$1" && c="${c} bg-warning"
	local x="$3"
	[ -n "$x" ] && x=" ${x}"
	local u="$4"
	[ -n "$u" ] && l="${l}, <span class=\"units text-secondary x-small\">$u</span>"
	echo "<label for=\"${1}\" class=\"${c}\"${x}>${l}</label>"
}

link_to() {
	echo "<a href=\"${2}\">${1}</a>"
}

load_plugins() {
	local i
	local n
	local p
	for i in $(ls -1 plugin-*); do
		# get plugin name
		p="$(sed -r -n '/^plugin=/s/plugin="(.*)"/\1/p' $i)"

		# hide unsupported plugins
		[ "$p" = "mqtt" ] && [ ! -f /usr/bin/mosquitto_pub ] && continue
		[ "$p" = "telegrambot" ] && [ ! -f /usr/bin/jsonfilter ] && continue
		[ "$p" = "zerotier" ] && [ ! -f /usr/sbin/zerotier-cli ] && continue

		# get plugin description
		n="$(sed -r -n '/^plugin_name=/s/plugin_name="(.*)"/\1/p' $i)"

		# check if plugin is enabled
		echo -n "<li><a class=\"dropdown-item"
		grep -q -s "^${p}_enabled=\"true\"" ${ui_config_dir}/${p}.conf && echo -n " plugin-enabled"
		echo "\" href=\"${i}\">${n}</a></li>"
	done
}

log() {
	echo $1 >/tmp/webui.log
}

majestic_diff() {
	config_file=/etc/majestic.yaml
	diff /rom$config_file $config_file >/tmp/majestic.patch
	cat /tmp/majestic.patch
}

# select_option "name" "value"
select_option() {
	local v=$2
	[ -z "$v" ] && v=$1
	local s=""
	[ "$v" = eval \$$v ] && $s=" selected"
	echo "<option value=\"${v}\"${s}>${1}</label>"
}

# pre "text" "classes" "extras"
pre() {
	# replace <, >, &, ", and ' with HTML entities
	tag "pre" "$(echo -e "$1" | sed "s/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g;s/\"/\&quot;/g")" "$2" "$3"
}

preview() {
	local refresh_rate=1
	[ -n "$1" ] && refresh_rate=$1
	[ "$debug" -gt 0 ] && refresh_rate=$(( refresh_rate * 100 ))
	if [ "true" = "$(yaml-cli -g .jpeg.enabled)" ]; then
		echo "<canvas id=\"preview\" style=\"background:gray url(/a/SMPTE_Color_Bars_16x9.svg);background-size:cover;width:100%;height:auto;\"></canvas>"
	else
		echo "<p class=\"alert alert-warning\"><a href=\"majestic-settings.cgi?tab=jpeg\">Enable JPEG support</a> to see the preview.</p>"
	fi
	echo "<script>
function calculatePreviewSize() {
  const i = new Image();
  i.src = pimg;
  i.onload = function() {
    ratio = i.naturalWidth / i.naturalHeight;
    pw = canvas.clientWidth
    pw -= pw % 16
    ph = pw / ratio
    ph -= ph % 16
    canvas.width = pw;
    canvas.height = ph;
    updatePreview();
  }
}

async function updatePreview() {
  if (typeof(pw) != 'undefined' && typeof(ph) != 'undefined') {
    jpg.src = pimg + '?width=' + pw + '&height=' + ph + '&qfactor=50&t=' + Date.now();
  } else {
    jpg.src = pimg + '?qfactor=50&t=' + Date.now();
  }
  jpg.onload = function() {
    ctx.drawImage(jpg, 0, 0, jpg.width, jpg.height, 0, 0, pw, ph);
    canvas.style.background = null;
  }
}

const l = document.location;
const pimg = '/cgi-bin/image.cgi';
const jpg = new Image();
jpg.addEventListener('load', async function() {
  await sleep(${refresh_rate} * 1000);
  updatePreview();
});

const canvas = \$('#preview');
const ctx = canvas.getContext('2d');
let pw, ph, ratio;
calculatePreviewSize();
</script>
"
}

progressbar() {
	local c="primary"
	[ "$1" -ge "75" ] && c="danger"
	echo "<div class=\"progress\" role=\"progressbar\" aria-valuenow=\"${1}\" aria-valuemin=\"0\" aria-valuemax=\"100\">" \
		"<div class=\"progress-bar progress-bar-striped progress-bar-animated bg-${c}\" style=\"width:${1}%\"></div>" \
		"</div>"
}

# redirect_back "flash class" "flash text"
redirect_back() {
	redirect_to "${HTTP_REFERER:-/}" "$1" "$2"
}

# redirect_to "url" "flash class" "flash text"
redirect_to() {
	[ -n "$3" ] && flash_save "$2" "$3"
	echo "HTTP/1.1 303 See Other
Content-type: text/html; charset=UTF-8
Cache-Control: no-store
Pragma: no-cache
Date: $(time_http)
Server: $SERVER_SOFTWARE
Location: $1

"
	exit 0
}

reload_locale() {
	local l
	[ -f /etc/webui/locale ] && l="$(cat /etc/webui/locale)"
	if [ -n "$l" ] && [ -f "/var/www/lang/${l}.sh" ]; then
		. "/var/www/lang/${l}.sh"
		locale="$l"
	else
		locale="en"
	fi
}

report_error() {
	echo "<h4 class=\"text-danger\">Oops. Something happened.</h4>"
	alert "$1" "danger"
}

# report_log "text" "extras"
report_log() {
	pre "$1" "small" "$2"
}

report_command_error() {
	echo "<h4 class=\"text-danger\">Oops. Something happened.</h4>"
	echo "<div class=\"alert alert-danger\">"
	report_command_info "$1" "$2"
	echo "</div>"
}

report_command_info() {
	echo "<h4># ${1}</h4>"
	echo "<pre class=\"small\">${2}</pre>"
}

# row_ "class"
row_() {
	echo "<div class\"row ${1}\" ${2}>"
}

_row() {
	echo "</div>"
}

row() {
	row_ "$2"
	echo "$1"
	_row
}

sanitize() {
	local n=$1
	# strip trailing whitespace
	eval $n=$(echo \$${n})
	# escape doublequotes
	eval $n=$(echo \${$n//\\\"/\\\\\\\"})
	# escape varialbles
	eval $n=$(echo \${$n//\$/\\\\\$})
}

sanitize4web() {
	local n=$1
	# convert html entities
	eval $n=$(echo \${$n//\\\"/\&quot\;})
	eval $n=$(echo \${$n//\$/\\\$})
}

set_error_flag() {
	flash_append "danger" "$1"
	error=1
}

generate_signature() {
	echo "${soc} (${soc_family} family), $sensor, ${flash_size} MB ${flash_type} flash, ${fw_version}-${fw_variant}, ${network_hostname}, ${network_macaddr}" >$signature_file
}

signature() {
	[ ! -f "$signature_file" ] && generate_signature
	cat $signature_file
}

tab_lap() {
	local c=""
	local s="false"
	[ -n "$3" ] && s="true" && c=" active"
	echo "<li class=\"nav-item\" role=\"presentation\">" \
		"<button role=\"tab\" id=\"#${1}-tab\" class=\"nav-link${c}\" data-bs-toggle=\"tab\" data-bs-target=\"#${1}-tab-pane\" aria-controls=\"${1}-tab-pane\" aria-selected=\"${s}\">${2}</button>" \
		"</li>"
}

t_label() {
	eval "echo \$tL_${1}"
}

t_value() {
	# eval "echo \"\$${1}\""
	eval echo '$'${1}
}

update_caminfo() {
	# Debug flag
	debug=$(fw_printenv -n debug); [ -z "$debug" ] && debug="0"

	local tmpfile=${ui_tmp_dir}/sysinfo.tmp
	:>$tmpfile
	# add all web-related config files
	# do not include ntp
	for _f in admin email ftp motion socks5 speaker telegram webhook yadisk; do
		[ -f "${ui_config_dir}/${_f}.conf" ] && cat "${ui_config_dir}/${_f}.conf" >>$tmpfile
	done; unset _f

	# Hardware
	flash_type=$(ipcinfo --flash-type)

	mtd_size=$(grep -E "nor|nand" $(ls /sys/class/mtd/mtd*/type) | sed -E "s|type.+|size|g")
	flash_size=$(awk '{sum+=$1} END{print sum/1024/1024}' $mtd_size)

	sensor_ini=$(ipcinfo --long-sensor)
	[ -z "$sensor_ini" ] && sensor_ini=$(fw_printenv -n sensor)

	sensor=$(ipcinfo --short-sensor)
	[ -z "$sensor" ] && sensor=$(echo $sensor_ini | cut -d_ -f1)

	soc_vendor=$(ipcinfo --vendor)

	soc=$(ipcinfo --chip-name)
	if [ -z "$soc" ] || [ "unknown" = "$soc" ] || [ "sigmastar" = "$soc_vendor" ]; then
		soc=$(fw_printenv -n soc)
	fi

	soc_family=$(ipcinfo --family)
	if [ "unknown" = "$soc_family" ] && [ "t20" = "$soc" ]; then
		soc_family="t21"
	fi

	# ipcinfo reports to stderr
	if [ "Temperature cannot be retrieved" = "$(ipcinfo --temp 2>&1)" ]; then
		soc_has_temp="false"
	else
		soc_has_temp="true"
	fi

	# Firmware
	uboot_version=$(fw_printenv -n ver)
	[ -z "$uboot_version" ] && uboot_version=$(strings /dev/mtdblock0 | grep '^U-Boot \d' | head -1)
	fw_version=$(grep "OPENIPC_VERSION" /etc/os-release | cut -d= -f2 | tr -d /\"/)
	fw_variant=$(grep "BUILD_OPTION" /etc/os-release | cut -d= -f2 | tr -d /\"/); [ -z "$fw_variant" ] && fw_variant="lite"
	fw_build=$(grep "GITHUB_VERSION" /etc/os-release | cut -d= -f2 | tr -d /\"/)
	mj_version=$($mj_bin_file -v)

	# WebUI version
	ui_version="bundled"; [ -f /var/www/.version ] && ui_version=$(cat /var/www/.version)
	ui_password=$(grep root /etc/shadow|cut -d: -f2)

	# Network
	network_dhcp="false"
	if [ -f /etc/resolv.conf ]; then
		network_dns_1=$(cat /etc/resolv.conf | grep nameserver | sed -n 1p | cut -d' ' -f2)
		network_dns_2=$(cat /etc/resolv.conf | grep nameserver | sed -n 2p | cut -d' ' -f2)
	fi
	network_hostname=$(hostname -s)
	network_interfaces=$(/sbin/ifconfig | grep '^\w' | awk {'print $1'} | tr '\n' ' ' | sed 's/ $//' | sed -E 's/\blo\b\s?//')

	# if no default interface then no gateway nor wan mac present
	network_default_interface=$(ip r | sed -nE '/default/s/.+dev (\w+).+?/\1/p' | head -n 1)
	if [ -n "$network_default_interface" ]; then
		[ "$(cat /etc/network/interfaces.d/${network_default_interface} | grep inet | grep dhcp)" ] && network_dhcp="true"
		network_gateway=$(ip r | sed -nE "/default/s/.+ via ([0-9\.]+).+?/\1/p")
	else
		network_default_interface=$(ip r | sed -nE 's/.+dev (\w+).+?/\1/p' | head -n 1)
		network_gateway='' # $(fw_printenv -n gatewayip) # FIXME: Why do we need this?
		# network_macaddr=$(fw_printenv -n ethaddr)      # FIXME: Why do we need this?
		# network_address=$(fw_printenv -n ipaddr)       # FIXME: Maybe use $(hostname -i) that would return 127.0.1.1?
		# network_netmask=$(fw_printenv -n netmask)
	fi
	network_macaddr=$(cat /sys/class/net/${network_default_interface}/address)
	network_address=$(ip r | sed -nE "/${network_default_interface}/s/.+src ([0-9\.]+).+?/\1/p" | uniq)
	network_cidr=$(ip r | sed -nE "/${network_default_interface}/s/^[0-9\.]+(\/[0-9]+).+?/\1/p")
	network_netmask=$(ifconfig $network_default_interface | grep "Mask:" | cut -d: -f4) # FIXME: Maybe convert from $network_cidr?

	overlay_root=$(mount | grep upperdir= | sed -r 's/^.*upperdir=([a-z\/]+).+$/\1/')

	# Default timezone is GMT
	tz_data=$(cat /etc/TZ)
	tz_name=$(cat /etc/timezone)
	if [ -z "$tz_data" ] || [ -z "$tz_name" ]; then
		tz_data="GMT0"; echo "$tz_data" >/etc/TZ
		tz_name="Etc/GMT"; echo "$tz_name" >/etc/timezone
	fi

	local variables="flash_size flash_type fw_version fw_variant fw_build
network_address network_cidr network_default_interface network_dhcp network_dns_1
network_dns_2 network_gateway network_hostname network_interfaces network_macaddr network_netmask
overlay_root mj_version soc soc_family soc_has_temp soc_vendor sensor sensor_ini tz_data tz_name
uboot_version ui_password ui_version"
	local v
	for v in $variables; do
		eval "echo ${v}=\'\$${v}\'>>${tmpfile}"
	done
	# sort content alphabetically
	sort <$tmpfile | sed /^$/d >$sysinfo_file && rm $tmpfile && unset tmpfile

	echo -e "debug=\"$debug\"\n# caminfo $(date +"%F %T")\n" >>$sysinfo_file
}

update_uboot_env() {
	local name="$1"
	local value="$2"
	[ "$value" != "$(fw_printenv -n $name)" ] && fw_setenv $name $value
}

xl() {
	local c="$1"
	echo "<b>${c}</b>"
	local o=$($c 2>&1)
	[ $? -ne 0 ] && error=1
	[ -n "$o" ] && echo "<div class=\"x-small p-3\"><i>${o}</i></div>"
}

d() {
	echo "$1" >&2
}

dump() {
	echo "Content-Type: text/plain; charset=UTF-8
Date: $(time_http)
Pragma: no-cache
Connection: close

--------------------
$(env|sort)
--------------------
"
	for x in $1; do
		echo -e "$x = $(eval echo \$$x)\n"
	done
	exit
}

include() {
	[ -f "$1" ] && . "$1"
}

ui_tmp_dir=/tmp/webui
ui_config_dir=/etc/webui

mj_bin_file=/usr/bin/majestic
flash_file=/tmp/webui-flash.txt
signature_file=/tmp/webui/signature.txt
sysinfo_file=/tmp/sysinfo.txt

[ ! -d $ui_tmp_dir ] && mkdir -p $ui_tmp_dir
[ ! -d $ui_config_dir ] && mkdir -p $ui_config_dir

lang_path=/var/www/lang/
[ ! -d $lang_path ] && mkdir -p $lang_path

[ ! -f $sysinfo_file ] && update_caminfo
include $sysinfo_file

pagename=$(basename "$SCRIPT_NAME")
pagename="${pagename%%.*}"

include p/locale_en.sh
include p/mj.cgi
include /etc/webui/mqtt.conf
include /etc/webui/socks5.conf
include /etc/webui/speaker.conf
include /etc/webui/telegram.conf
include /etc/webui/webhook.conf
include /etc/webui/webui.conf
include /etc/webui/yadisk.conf

# reload_locale

# FIXME: mandatory password change disabled for testing purposes
check_password
get_soc_temp
%>
