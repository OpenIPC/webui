#!/usr/bin/haserl
<%
IFS_ORIG=$IFS

# tag "tag" "text" "css" "extras"
tag() {
  local _t="$1"
  local _n="$2"
  local _c="$3"
  local _x="$4"
  [ -n "$_c" ] && _c=" class=\"${_c}\""
  [ -n "$_x" ] && _x=" ${_x}"
  echo "<${_t}${_c}${_x}>${_n}</${_t}>"
}

# A "tag" "classes" "extras"
A() {
  local _c="$2"; [ -n "$_c" ] && _c=" class=\"${_c}\""
  local _x="$3"; [ -n "$_x" ] && _x=" ${_x}"
  echo "<${1}${_c}${_x}>"
}

Z() {
  echo "</${1}>"
}

# tag "text" "classes" "extras"
div()   { tag "div"   "$1" "$2" "$3"; }
h1()    { tag "h1"    "$1" "$2" "$3"; }
h2()    { tag "h2"    "$1" "$2" "$3"; }
h3()    { tag "h3"    "$1" "$2" "$3"; }
h4()    { tag "h4"    "$1" "$2" "$3"; }
h5()    { tag "h5"    "$1" "$2" "$3"; }
h6()    { tag "h6"    "$1" "$2" "$3"; }
label() { tag "label" "$1" "$2" "$3"; }
li()    { tag "li"    "$1" "$2" "$3"; }
p()     { tag "p"     "$1" "$2" "$3"; }
span()  { tag "span"  "$1" "$2" "$3"; }

div_() { A "div" "$1" "$2"; }
_div() { Z "div"; }

span_() { A "span" "$1" "$2"; }
_span() { Z "span"; }

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
  echo "<form action=\"majestic-config-actions.cgi\" method=\"post\">" \
    "<input type=\"hidden\" name=\"action\" value=\"backup\">"
  button_submit "Backup settings"
  echo "</form>"
}

button_mj_reset() {
  echo "<form action=\"majestic-config-actions.cgi\" method=\"post\">" \
    "<input type=\"hidden\" name=\"action\" value=\"reset\">"
  button_submit "Reset Majestic" "danger"
  echo "</form>"
}

button_reboot() {
  echo "<form action=\"reboot.cgi\" method=\"post\">" \
    "<input type=\"hidden\" name=\"action\" value=\"reboot\">"
  button_submit "Reboot camera" "danger"
  echo "</form>"
}

button_refresh() {
  echo "<a href=\"${REQUEST_URI}\" class=\"btn btn-primary refresh\">Refresh</a>"
}

button_reset_firmware() {
  echo "<form action=\"firmware-reset.cgi\" method=\"post\">" \
    "<input type=\"hidden\" name=\"action\" value=\"reset\">"
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
  local _t="$1"; [ -z "$_t" ] && _t="Save changes"
  local _c="$2"; [ -z "$_c" ] && _c="primary"
  local _x="$3"; [ -z "$_x" ] && _x=" ${_x}"
  echo "<div class=\"mt-2\"><input type=\"submit\" class=\"btn btn-${_c}\"${_x} value=\"${_t}\"></div>"
}

button_webui_log() {
  [ -f "/tmp/webui.log" ] &&
    link_to "Download log file" "dl.cgi?file=/tmp/webui.log"
}

check_file_exist() {
  [ ! -f "$1" ] &&
    redirect_back "danger" "File ${1} not found"
}

check_password() {
  _safepage="/cgi-bin/webui-settings.cgi"
  [ "0${debug}" -ge "1" ] && return
  [ -z "$REQUEST_URI" ] || [ "$REQUEST_URI" = "${_safepage}" ] && return
  if [ ! -f /etc/shadow- ] || [ -z $(grep root /etc/shadow- | cut -d: -f2) ]; then
    redirect_to "${_safepage}" "danger" "You must set your own secure password!"
  fi
}

e() {
  echo -e -n "$1"
}

ex() {
  # NB! $() forks process and stalls output.
  echo "<div class=\"${2}\">"
  echo "<h6># ${1}</h6><pre class=\"small\">"
  eval "$1" | sed "s/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g;s/\"/\&quot;/g"
  echo "</pre>"
  echo "</div>"
}

# field_checkbox "name" "label" "hint"
field_checkbox() {
  local _l=$2
  [ -z "$_l" ] && _l="$(t_label "$1")"
  [ -z "$_l" ] && _l="<span class=\"bg-warning\">${1}</span>"
  local _h=$3
  local _v=$(t_value "$1")
  [ -z "$_v" ] && _v="false"
  echo "<p class=\"boolean form-check\">" \
    "<input type=\"hidden\" id=\"${1}-false\" name=\"${1}\" value=\"false\">" \
    "<input type=\"checkbox\" name=\"${1}\" id=\"${1}\" value=\"true\" class=\"form-check-input\"$(t_checked "true" "$_v")>" \
    "<label for=\"${1}\" class=\"form-label\">${_l}</label>"
  [ -n "$_h" ] && echo "<span class=\"hint text-secondary d-block mb-2\">${_h}</span>"
  echo "</p>"
}

# field_file "name" "label" "hint"
field_file() {
  local _l=$2
  [ -z "$_l" ] && _l="$(t_label "$1")"
  [ -z "$_l" ] && _l="<span class=\"bg-warning\">${1}</span>"
  local _h=$3
  echo "<p class=\"file\">" \
    "<label for=\"${1}\" class=\"form-label\">${_l}</label>" \
    "<input type=\"file\" id=\"${1}\" name=\"${1}\" class=\"form-control\">"
  [ -n "$_h" ] && echo "<span class=\"hint text-secondary\">${_h}</span>"
  echo "</p>"
}

# field_hidden "name" "value"
field_hidden() {
  # do we need id here? id=\"${1}\". We do for netip password!
  echo "<input type=\"hidden\" name=\"${1}\" id=\"${1}\" value=\"${2}\" class=\"form-hidden\">"
}

# field_number "name" "label" "range" "hint"
field_number() {
  local _n=$1
  local _l=$2
  [ -z "$_l" ] && _l="$(t_label "$1")"
  [ -z "$_l" ] && _l="<span class=\"bg-warning\">${1}</span>"
  local _r=$3 # min,max,step,button
  local _mn=$(echo "$_r" | cut -d, -f1)
  local _mx=$(echo "$_r" | cut -d, -f2)
  local _st=$(echo "$_r" | cut -d, -f3)
  local _ab=$(echo "$_r" | cut -d, -f4)
  local _h=$4
  local _v=$(t_value "$_n")
  local _vr=$_v
  [ -n "$_ab" ] && [ "$_ab" = "$_v" ] && _vr=$(( ( $_mn + $_mx ) / 2 ))
  echo "<p class=\"number\">" \
    "<label class=\"form-label\" for=\"${_n}\">${_l}</label>" \
    "<span class=\"input-group\">"
  # NB! no name on checkbox, since we don't want its data submitted
  [ -n "$_ab" ] && echo "<label class=\"input-group-text\" for=\"${_n}-auto\">${_ab}" \
    "<input type=\"checkbox\" class=\"form-check-input auto-value ms-1\" id=\"${_n}-auto\"" \
      " data-for=\"${_n}\" data-value=\"${_vr}\" $(t_checked "$_ab" "$_v")>" \
    "</label>"
  echo "<input type=\"number\" id=\"${_n}\" name=\"${_n}\" class=\"form-control text-end\"" \
      " value=\"${_vr}\" min=\"${_mn}\" max=\"${_mx}\" step=\"${_st}\">" \
    "</span>"
  [ -n "$_h" ] && echo "<span class=\"hint text-secondary\">${_h}</span>"
  echo "</p>"
}

# field_password "name" "label" "hint"
field_password() {
  local _l=$2
  [ -z "$_l" ] && _l="$(t_label "$1")"
  [ -z "$_l" ] && _l="<span class=\"bg-warning\">${1}</span>"
  local _h=$3
  local _v=$(t_value "$1")
  echo "<p class=\"password\" id=\"${1}_wrap\">" \
    "<label for=\"${1}\" class=\"form-label\">${_l}</label>" \
    "<span class=\"input-group\">" \
    "<input type=\"password\" id=\"${1}\" name=\"${1}\" class=\"form-control\" value=\"${_v}\" placeholder=\"K3wLHaZk3R!\">" \
    "<label class=\"input-group-text\">" \
    "<input type=\"checkbox\" class=\"form-check-input me-1\" data-for=\"${1}\"> show" \
    "</label>" \
    "</span>"
  [ -n "$_h" ] && echo "<span class=\"hint text-secondary\">${_h}</span>"
  echo "</p>"
}

# field_range "name" "label" "range" "hint"
field_range() {
  local _n=$1
  local _l=$2
  [ -z "$_l" ] && _l="$(t_label "$_n")"
  [ -z "$_l" ] && _l="<span class=\"bg-warning\">${_n}</span>"
  local _r=$3 # min,max,step,button
  local _mn=$(echo "$_r" | cut -d, -f1)
  local _mx=$(echo "$_r" | cut -d, -f2)
  local _st=$(echo "$_r" | cut -d, -f3)
  local _ab=$(echo "$_r" | cut -d, -f4)
  local _h=$4
  local _v=$(t_value "$_n")
  local _vr=$_v
  [ -z "$_vr" -o "$_ab" = "$_vr" ] && _vr=$(( ( $_mn + $_mx ) / 2 ))
  echo "<p class=\"range\" id=\"${_n}_wrap\">" \
    "<label class=\"form-label\" for=\"${_n}\">${_l}</label>" \
    "<span class=\"input-group\">"
  # NB! no name on checkbox, since we don't want its data submitted
  [ -n "$_ab" ] && echo "<label class=\"input-group-text\" for=\"${_n}-auto\">${_ab}" \
    "<input type=\"checkbox\" class=\"form-check-input auto-value ms-1\" id=\"${_n}-auto\"" \
      " data-for=\"${_n}\" data-value=\"${_vr}\" $(t_checked "$_ab" "$_v")>" \
    "</label>"
  # Input that holds the submitting value.
  echo "<input type=\"hidden\" name=\"${_n}\" id=\"${_n}\" value=\"${_v}\">"
  # NB! no name on range, since we don't want its data submitted
  echo "<input type=\"range\" class=\"form-control form-range\" id=\"${_n}-range\"" \
      "value=\"${_vr}\" min=\"${_mn}\" max=\"${_mx}\" step=\"${_st}\">"
  echo "<span class=\"input-group-text show-value\" id=\"${_n}-show\">${_vr}</span>" \
    "</span>"
  [ -n "$_h" ] && echo "<span class=\"hint text-secondary\">${_h}</span>"
  echo "</p>"
}

# field_select "name" "label" "options" "hint" "units"
field_select() {
  local _l=$2
  [ -z "$_l" ] && _l="$(t_label "$1")"
  [ -z "$_l" ] && _l="<span class=\"bg-warning\">${1}</span>"
  local _o=$3
  _o=${_o//,/ }
  local _h=$4
  local _u=$5
  echo "<p class=\"select\" id=\"${1}_wrap\">" \
    "<label for=\"${1}\" class=\"form-label\">${_l}</label>" \
    "<select class=\"form-select\" id=\"${1}\" name=\"${1}\">"
  [ -z "$(t_value "$1")" ] && echo "<option value=\"\">Select from available options</option>"
  for o in $_o; do
    _v="${o%:*}"
    _n="${o#*:}"
    [ "$1" != "mj_isp_sensorConfig" ] && _n=${_n//_/ }
    echo -n "<option value=\"${_v}\""
    [ "$(t_value "$1")" = "$_v" ] && echo -n " selected"
    echo ">${_n}</option>"
    unset _v; unset _n
  done
  echo "</select>"
  [ -n "$_u" ] && echo "<span class=\"input-group-text\">${_u}</span>"
  [ -n "$_h" ] && echo "<span class=\"hint text-secondary\">${_h}</span>"
  echo "</p>"
}

# field_swith "name" "label" "hint" "options"
field_switch() {
  local _l=$2
  [ -z "$_l" ] && _l="$(t_label "$1")"
  [ -z "$_l" ] && _l="<span class=\"bg-warning\">$1</span>"
  local _v=$(t_value "$1"); [ -z "$_v" ] && _v="false"
  local _h="$3"
  local _o=$4; [ -z "$_o" ] && _o="true,false"
  local _o1=$(echo "$_o" | cut -d, -f1)
  local _o2=$(echo "$_o" | cut -d, -f2)
  echo "<p class=\"boolean\">" \
    "<span class=\"form-check form-switch\">" \
    "<input type=\"hidden\" id=\"${1}-false\" name=\"${1}\" value=\"${_o2}\">" \
    "<input type=\"checkbox\" id=\"${1}\" name=\"${1}\" value=\"${_o1}\" role=\"switch\"" \
      " class=\"form-check-input\"$(t_checked "$_o1" "$_v")>" \
    "<label for=\"$1\" class=\"form-check-label\">${_l}</label>" \
    "</span>"
  [ -n "$_h" ] && echo "<span class=\"hint text-secondary\">${_h}</span>"
  echo "</p>"
}

# field_text "name" "label" "hint" "placeholder"
field_text() {
  local _l=$2
  [ -z "$_l" ] && _l="$(t_label "$1")"
  [ -z "$_l" ] && _l="<span class=\"bg-warning\">$1</span>"
  local _v="$(t_value "$1")"
  local _h="$3"
  local _p="$4"
  echo "<p class=\"string\" id=\"${1}_wrap\">" \
    "<label for=\"${1}\" class=\"form-label\">${_l}</label>" \
    "<input type=\"text\" id=\"${1}\" name=\"${1}\" class=\"form-control\" value=\"${_v}\" placeholder=\"${_p}\">"
  [ -n "$_h" ] && echo "<span class=\"hint text-secondary\">${_h}</span>"
  echo "</p>"
}

# field_textarea "name" "label" "hint"
field_textarea() {
  local _l=$2
  [ -z "$_l" ] && _l="$(t_label "$1")"
  [ -z "$_l" ] && _l="<span class=\"bg-warning\">$1</span>"
  local _v=$(t_value "$1")
  local _h=$3
  echo "<p class=\"textarea\" id=\"${1}_wrap\">" \
    "<label for=\"${1}\" class=\"form-label\">${_l}</label>" \
    "<textarea id=\"${1}\" name=\"${1}\" class=\"form-control\">${_v}</textarea>"
  [ -n "$_h" ] && echo "<span class=\"hint text-secondary\">${_h}</span>"
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
  local _c
  local _m
  local _l
  OIFS="$IFS"
  IFS=$'\n'
  for _l in $(cat "$flash_file"); do
    _c="$(echo $_l | cut -d':' -f1)"
    _m="$(echo $_l | cut -d':' -f2-)"
    echo "<div class=\"alert alert-${_c} alert-dismissible fade show\" role=\"alert\">" \
      "${_m}" \
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
  local _c="form-label"
  [ -n "$2" ] && _c="${_c} ${2}"
  local _l="$(t_label "$1")"
  [ -z "$_l" ] && _l="$1" && _c="${_c} bg-warning"
  local _x="$3"
  [ -n "$_x" ] && _x=" ${_x}"
  local _u="$4"
  [ -n "$_u" ] && _l="${_l}, <span class=\"units text-secondary x-small\">$_u</span>"
  echo "<label for=\"${1}\" class=\"${_c}\"${_x}>${_l}</label>"
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
    [ "$p" = "mqtt"        ] && [ ! -f /usr/bin/mosquitto_pub ] && continue
    [ "$p" = "telegrambot" ] && [ ! -f /usr/bin/jsonfilter    ] && continue
    [ "$p" = "zerotier"    ] && [ ! -f /usr/sbin/zerotier-cli ] && continue

    # get plugin description
    n="$(sed -r -n '/^plugin_name=/s/plugin_name="(.*)"/\1/p' $i)"

    # check if plugin is enabled
    echo -n "<li><a class=\"dropdown-item"
    grep -q "^${p}_enabled=\"true\"" ${ui_config_dir}/${p}.conf && echo -n " plugin-enabled"
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
  local _v=$2
  [ -z "$_v" ] && _v=$1
  local _s=""
  [ "$_v" = eval \$$_v ] && $s=" selected"
  echo "<option value=\"${_v}\"${_s}>${1}</label>"
}

# pre "text" "classes" "extras"
pre() {
  # replace <, >, &, ", and ' with HTML entities
  tag "pre" "$(echo -e "$1" | sed "s/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g;s/\"/\&quot;/g")" "$2" "$3"
}

preview() {
  local refresh_rate=10
  [ -n "$1" ] && refresh_rate=$1
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
  local -l
  [ -f /etc/webui/locale ] && _l="$(cat /etc/webui/locale)"
  if [ -n "$_l" ] && [ -f "/var/www/lang/${_l}.sh" ]; then
    source "/var/www/lang/${_l}.sh"
    locale="$_l"
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
  local _n=$1
  # strip trailing whitespace
  eval $_n=$(echo \$${_n})
  # escape doublequotes
  eval $_n=$(echo \${$_n//\\\"/\\\\\\\"})
  # escape varialbles
  eval $_n=$(echo \${$_n//\$/\\\\\$})
}

sanitize4web() {
  local _n=$1
  # convert html entities
  eval $_n=$(echo \${$_n//\\\"/\&quot\;})
  eval $_n=$(echo \${$_n//\$/\\\$})
}

generate_signature() {
  echo "${soc} (${soc_family} family), $sensor, ${flash_size} MB ${flash_type} flash, ${fw_version}-${fw_variant}, ${network_hostname}, ${network_macaddr}" >$signature_file
}

signature() {
  [ ! -f "$signature_file" ] && generate_signature
  cat $signature_file
}

tab_lap() {
  local _c=""
  local _s="false"
  [ -n "$3" ] && _s="true" && _c=" active"
  echo "<li class=\"nav-item\" role=\"presentation\">" \
    "<button role=\"tab\" id=\"#${1}-tab\" class=\"nav-link${_c}\"" \
    " data-bs-toggle=\"tab\" data-bs-target=\"#${1}-tab-pane\"" \
    " aria-controls=\"${1}-tab-pane\" aria-selected=\"${_s}\">${2}</button></li>"
}

t_checked() {
  [ "$2" = "$1" ] && echo " checked"
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

  _tmpfile=${ui_tmp_dir}/sysinfo.tmp
  :>$_tmpfile
  # add all web-related config files
  # do not include ntp
  for _f in admin email ftp motion socks5 speaker telegram webhook yadisk; do
    [ -f "${ui_config_dir}/${_f}.conf" ] && cat "${ui_config_dir}/${_f}.conf" >>$_tmpfile
  done; unset _f

  # Hardware
  flash_type=$(ipcinfo --flash-type)

  flash_size=$(awk '{sum+=sprintf("0x%s", $2);} END{print sum/1048576;}' /proc/mtd)

  sensor_ini=$(ipcinfo --long-sensor)
  [ -z "$sensor_ini" ] && sensor_ini=$(fw_printenv -n sensor)

  sensor=$(ipcinfo --short-sensor)
  if [ -z "$sensor" ]; then
    sensor=$(echo $sensor_ini | cut -d_ -f1)
  fi

  soc=$(ipcinfo --chip-name)
  if [ -z "$soc" ] || [ "unknown" = "$soc" ]; then
    soc=$(fw_printenv -n soc)
  fi

  soc_family=$(ipcinfo --family)
  if [ "unknown" = "$soc_family" ] && [ "t20" = "$soc" ]; then
    soc_family="t21"
  fi

  soc_vendor=$(ipcinfo --vendor)

  # ipcinfo reports to stderr
  if [ "Temperature cannot be retrieved" = "$(ipcinfo --temp 2>&1)" ]; then
    soc_has_temp="false"
  else
    soc_has_temp="true"
  fi

  # Firmware
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

  local _vars="flash_size flash_type fw_version fw_variant fw_build
network_address network_cidr network_default_interface network_dhcp network_dns_1
network_dns_2 network_gateway network_hostname network_interfaces network_macaddr network_netmask
overlay_root mj_version soc soc_family soc_has_temp soc_vendor sensor sensor_ini tz_data tz_name
ui_password ui_version"
  local v
  for _v in $_vars; do
    eval "echo ${_v}=\'\$${_v}\'>>${_tmpfile}"
  done
  # sort content alphabetically
  sort <$_tmpfile | sed /^$/d >$sysinfo_file && rm $_tmpfile && unset _tmpfile

  echo -e "debug=\"$debug\"\n# caminfo $(date +"%F %T")\n" >>$sysinfo_file
}

xl() {
  local _c="$1"
  echo "<b>${_c}</b>"
  local _o=$($_c 2>&1)
  [ $? -ne 0 ] && error=1
  [ -n "$_o" ] && echo "<div class=\"x-small p-3\"><i>${_o}</i></div>"
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
  for x in $1; do echo -e "$x = $(eval echo \$$x)\n"; done
  exit
}

include() {
  [ -f "$1" ] && source "$1"
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
