#!/usr/bin/haserl
<%
# tag "tag" "text" "css" "extras"
tag() {
  _t="$1"; _n="$2"; _c="$3"; _x="$4"
  [ -n "$_c" ] && _c=" class=\"${_c}\""
  [ -n "$_x" ] && _x=" ${_x}"
  echo "<${_t}${_c}${_x}>${_n}</${_t}>"
  unset _t; unset _n; unset _c; unset _x
}

# A "tag" "classes" "extras"
A() {
  _c="$2"; [ -n "$_c" ] && _c=" class=\"${_c}\""
  _x="$3"; [ -n "$_x" ] && _x=" ${_x}"
  echo "<${1}${_c}${_x}>"
  unset _c; unset _x
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

time_epoch() {
  if [ -n "$1" ]; then
    TZ=GMT0 date +%s --date="${1}"
  else
    TZ=GMT0 date +%s
  fi
}

time_http() {
  if [ -n "$1" ]; then
    TZ=GMT0 date +"%a, %d %b %Y %T %Z" --date="${1}"
  else
    TZ=GMT0 date +"%a, %d %b %Y %T %Z"
  fi
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

# button_submit "text" "type" "extras"
button_submit() {
  _t="$1"; [ -z "$_t" ] && _t="Save changes"
  _c="$2"; [ -z "$_c" ] && _c="primary"
  _x="$3"; [ -z "$_x" ] && _x=" ${_x}"
  echo "<div class=\"mt-2\"><input type=\"submit\" class=\"btn btn-${_c}\"${_x} value=\"${_t}\"></div>"
  unset _c; unset _t; unset _x
}

#check_password() {
#  [ "0${debug}" -ge "1" ] && return
#  [ -z "$REQUEST_URI" ] || [ "$REQUEST_URI" = "/cgi-bin/webui.cgi" ] && return
#  if [ -z "$ui_password" ] || [ "$ui_password_fw" = "$ui_password" ]; then
#    redirect_to "webui.cgi" "danger" "You must set your own secure password!"
#  fi
#}

e() {
  echo -e -n "$1"
}

ex() {
  # NB! $() forks process and stalls output.
  echo "<h5># ${1}</h5><pre class=\"small\">"
  eval "$1" | sed "s/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g;s/\"/\&quot;/g"
  echo "</pre>"
}

# field_checkbox "name" "label" "hint"
field_checkbox() {
  _l=$2
  [ -z "$_l" ] && _l="$(t_label "$1")"
  [ -z "$_l" ] && _l="<span class=\"bg-warning\">${1}</span>"

  _h=$3

  _v=$(t_value "$1")
  [ -z "$_v" ] && _v="false"

  echo "<p class=\"boolean form-check\">" \
    "<input type=\"hidden\" id=\"${1}-false\" name=\"${1}\" value=\"false\">" \
    "<input type=\"checkbox\" name=\"${1}\" id=\"${1}\" value=\"true\" class=\"form-check-input\"$(t_checked "true" "$_v")>" \
    "<label for=\"${1}\" class=\"form-label\">${_l}</label>"
  [ -n "$_h" ] && echo "<span class=\"hint text-secondary\">${_h}</span>"
  echo "</p>"
  unset _h; unset _l; unset _v
}

# field_file "name" "label" "hint"
field_file() {
  _l=$2
  [ -z "$_l" ] && _l="$(t_label "$1")"
  [ -z "$_l" ] && _l="<span class=\"bg-warning\">${1}</span>"

  _h=$3

  echo "<p class=\"file\">" \
    "<label for=\"${1}\" class=\"form-label\">${_l}</label>" \
    "<input type=\"file\" id=\"${1}\" name=\"${1}\" class=\"form-control\">"
  [ -n "$_h" ] && echo "<span class=\"hint text-secondary\">${_h}</span>"
  echo "</p>"
  unset _h; unset _l
}

# field_hidden "name" "value"
field_hidden() {
  # do we need id here? id=\"${1}\". We do for netip password!
  echo "<input type=\"hidden\" name=\"${1}\" id=\"${1}\" value=\"${2}\" class=\"form-hidden\">"
}

# field_number "name" "label" "range" "hint"
field_number() {
  _l=$2
  [ -z "$_l" ] && _l="$(t_label "$1")"
  [ -z "$_l" ] && _l="<span class=\"bg-warning\">${1}</span>"

  # min, max, step, button
  _r=$3
  _f=$(echo "$_r" | cut -d, -f1)
  _t=$(echo "$_r" | cut -d, -f2)
  _s=$(echo "$_r" | cut -d, -f3)
  _b=$(echo "$_r" | cut -d, -f4)

  _h=$4

  _v=$(t_value "$1")

  echo "<p class=\"number\">" \
    "<label for=\"${1}\" class=\"form-label\">${_l}</label>" \
    "<input type=\"number\" name=\"${1}\" id=\"${1}\" class=\"form-control text-end\"" \
      " value=\"${_v}\" min=\"${_f}\" max=\"${_t}\" step=\"${_s}\" value=\"${_v}\">"
  [ -n "$_h" ] && echo "<span class=\"hint text-secondary\">${_h}</span>"
  echo "</p>"
  unset _b; unset _f; unset _h; unset _l; unset _r; unset _s; unset _t; unset _v
}

# field_password "name" "label" "hint"
field_password() {
  _l=$2
  [ -z "$_l" ] && _l="$(t_label "$1")"
  [ -z "$_l" ] && _l="<span class=\"bg-warning\">${1}</span>"

  _h=$3

  _v=$(t_value "$1")

  echo "<p class=\"password\">" \
    "<label for=\"${1}\" class=\"form-label\">${_l}</label>" \
    "<span class=\"input-group\">" \
    "<input type=\"password\" id=\"${1}\" name=\"${1}\" class=\"form-control\" value=\"${_v}\" placeholder=\"K3wLHaZk3R!\">" \
    "<label class=\"input-group-text\">" \
    "<input type=\"checkbox\" class=\"form-check-input me-1\" data-for=\"${1}\"> show" \
    "</label>" \
    "</span>"
  [ -n "$_h" ] && echo "<span class=\"hint text-secondary\">${_h}</span>"
  echo "</p>"
  unset _h; unset _l; unset _v
}

# field_range "name" "label" "range" "hint"
field_range() {
  _n=$1

  _l=$2
  [ -z "$_l" ] && _l="$(t_label "$_n")"
  [ -z "$_l" ] && _l="<span class=\"bg-warning\">${_n}</span>"

  _r=$3 # min,max,step,button
  _mn=$(echo "$_r" | cut -d, -f1)
  _mx=$(echo "$_r" | cut -d, -f2)
  _st=$(echo "$_r" | cut -d, -f3)
  _ab=$(echo "$_r" | cut -d, -f4)

  _h=$4

  _v=$(t_value "$_n")

  _vr=$_v
  [ -z "$_vr" -o "$_ab" = "$_vr" ] && _vr=$(( ( $_mn + $_mx ) / 2 ))

  echo "<p class=\"range\">" \
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
  unset _ab; unset _h; unset _mn; unset _mx; unset _n; unset _r; unset _st; unset _v; unset _vr
}

# field_select "name" "label" "options" "hint" "units"
field_select() {
  _l=$2
  [ -z "$_l" ] && _l="$(t_label "$1")"
  [ -z "$_l" ] && _l="<span class=\"bg-warning\">${1}</span>"

  _o=$3
  _o=${_o//,/ }

  _h=$4

  _u=$5

  echo "<p class=\"select\">" \
    "<label for=\"${1}\" class=\"form-label\">${_l}</label>" \
    "<select class=\"form-select\" id=\"${1}\" name=\"${1}\">"
  [ -z "$(t_value "$1")" ] && echo "<option value=\"\">Select from available options</option>"
  for o in $_o; do
    _v="${o%|*}"
    _n="${o#*|}"
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
  unset _h; unset _l; unset _o; unset _u
}

# field_swith "name" "label" "hint" "options"
field_switch() {
  _l=$2
  [ -z "$_l" ] && _l="$(t_label "$1")"
  [ -z "$_l" ] && _l="<span class=\"bg-warning\">$1</span>"

  _h=$3

  _o=$4; [ -z "$_o" ] && _o="true,false"
  _o1=$(echo "$_o" | cut -d, -f1)
  _o2=$(echo "$_o" | cut -d, -f2)

  _v=$(t_value "$1"); [ -z "$_v" ] && _v="false"

  echo "<p class=\"boolean\">" \
    "<span class=\"form-check form-switch\">" \
    "<input type=\"hidden\" id=\"${1}-false\" name=\"${1}\" value=\"${_o2}\">" \
    "<input type=\"checkbox\" id=\"${1}\" name=\"${1}\" value=\"${_o1}\" role=\"switch\"" \
      " class=\"form-check-input\"$(t_checked "$_o1" "$_v")>" \
    "<label for=\"$1\" class=\"form-check-label\">${_l}</label>" \
    "</span>"
  [ -n "$_h" ] && echo "<span class=\"hint text-secondary\">${_h}</span>"
  echo "</p>"
  unset _h; unset _l; unset _o; unset _o1; unset _o2; unset _v
}

# field_text "name" "label" "hint"
field_text() {
  _l=$2
  [ -z "$_l" ] && _l="$(t_label "$1")"
  [ -z "$_l" ] && _l="<span class=\"bg-warning\">$1</span>"

  _h=$3

  _v="$(t_value "$1")"

  #  placeholder="FQDN or IP address"
  echo "<p class=\"string\">" \
    "<label for=\"${1}\" class=\"form-label\">${_l}</label>" \
    "<input type=\"text\" id=\"${1}\" name=\"${1}\" class=\"form-control\" value=\"${_v}\">"
  [ -n "$_h" ] && echo "<span class=\"hint text-secondary\">${_h}</span>"
  echo "</p>"
  unset _h; unset _l; unset _v
}

# field_textarea "name" "label" "hint"
field_textarea() {
  _l=$2
  [ -z "$_l" ] && _l="$(t_label "$1")"
  [ -z "$_l" ] && _l="<span class=\"bg-warning\">$1</span>"

  _h=$3

  _v=$(t_value "$1")

  echo "<p class=\"textarea\">" \
    "<label for=\"${1}\" class=\"form-label\">${_l}</label>" \
    "<textarea id=\"${1}\" name=\"${1}\" class=\"form-control\">${_v}</textarea>"
  [ -n "$_h" ] && echo "<span class=\"hint text-secondary\">${_h}</span>"
  echo "</p>"
  unset _h; unset _l; unset _v
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
  unset _c; unset _m
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
  [ -n "$1" ] && echo -n "$1 - "
  echo -n "OpenIPC"
}

# label "name" "classes" "extras" "units"
label() {
  _c="form-label"
  [ -n "$2" ] && _c="${_c} ${2}"

  _l="$(t_label "$1")"
  [ -z "$_l" ] && _l="$1" && _c="${_c} bg-warning"

  _x="$3"
  [ -n "$_x" ] && _x=" ${_x}"

  _u="$4"
  [ -n "$_u" ] && _l="${_l}, <span class=\"units text-secondary x-small\">$_u</span>"

  echo "<label for=\"${1}\" class=\"${_c}\"${_x}>${_l}</label>"
  unset _c; unset _l; unset _u; unset _x
}

load_plugins() {
  for i in $(ls -1 plugin-*); do
    eval "$(grep 'plugin_name=' $i)"
    echo "<li><a class=\"dropdown-item\" href=\"${i}\">${plugin_name}</a></li>"
    unset plugin_name
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
  _v=$2
  [ -z "$_v" ] && _v=$1
  _s=""; [ "$_v" = eval \$$_v ] && $s=" selected"
  echo "<option value=\"${_v}\"${_s}>${1}</label>"
}

# pre "text" "classes" "extras"
pre() {
  # replace <, >, &, ", and ' with HTML entities
  tag "pre" "$(echo -e "$1" | sed "s/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g;s/\"/\&quot;/g")" "$2" "$3"
}

preview() {
  if [ "true" = "$(yaml-cli -g .jpeg.enabled)" ]; then
    echo "<div class=\"ratio ratio-16x9 mb-3\"><img src=\"http://${network_address}/image.jpg\" alt=\"Image: preview\" class=\"img-fluid mb-3\" id=\"preview-jpeg\" width=\"1280\" height=\"720\"></div>"
  else
    echo "<p class=\"alert alert-warning\"><a href=\"majestic-settings.cgi?tab=jpeg\">Enable JPEG support</a> to see the preview.</p>"
  fi
  echo "<script>async function updatePreview() { await sleep(1000); \$('#preview-jpeg').src = 'http://${network_address}/image.jpg?t=' + Date.now(); } \$('#preview-jpeg').addEventListener('load', updatePreview); updatePreview();</script>"
}

progressbar() {
  _c="primary"; [ "$1" -ge "75" ] && _c="danger"
  echo "<div class=\"progress\">" \
    "<div class=\"progress-bar progress-bar-striped progress-bar-animated bg-${_c}\" role=\"progressbar\"" \
      " style=\"width:${1}%\" aria-valuenow=\"${1}\" aria-valuemin=\"0\" aria-valuemax=\"100\"></div>" \
    "</div>"
}

# redirect_back "flash class" "flash text"
redirect_back() {
  redirect_to "$HTTP_REFERER" "$1" "$2"
}

# redirect_to "url" "flash class" "flash text"
redirect_to() {
  [ -n "$3" ] && flash_save "$2" "$3"
  echo "HTTP/1.1 302 Moved Temporarily
Content-type: text/html; charset=UTF-8
Cache-Control: no-store
Pragma: no-cache
Date: $(time_http)
Location: $1
Server: $SERVER_SOFTWARE
Status: 302 Moved Temporarily
"
  exit 0
}

reload_locale() {
  [ -f /etc/web_locale ] && _l="$(cat /etc/web_locale)"
  if [ -n "$_l" ] && [ -f "/var/www/lang/${_l}.sh" ]; then
    source "/var/www/lang/${_l}.sh"
    locale="$_l"
  else
    locale="en"
  fi
  unset _l
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
  report_log "$2"
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
  _n=$1
  # strip trailing whitespace
  eval $_n=$(echo \$${_n})
  unset _n
}

generate_signature() {
  echo "${soc} (${soc_family} family), $sensor, ${flash_size} MB Flash, ${fw_version}-${fw_variant}, ${network_hostname}, ${network_wan_mac}" >$signature_file
}

signature() {
  [ ! -f "$signature_file" ] && generate_signature
  cat $signature_file
}

tab_lap() {
  _c=""; _s="false"; [ -n "$3" ] && _s="true" && _c=" active"
  echo "<li class=\"nav-item\" role=\"presentation\">" \
    "<button role=\"tab\" id=\"#${1}-tab\" class=\"nav-link${_c}\"" \
    " data-bs-toggle=\"tab\" data-bs-target=\"#${1}-tab-pane\"" \
    " aria-controls=\"${1}-tab-pane\" aria-selected=\"${_s}\">${2}</button></li>"
   unset _c; unset _s
}

t_checked() {
  [ "$2" = "$1" ] && echo "checked"
}

t_label() {
  eval "echo \$tL_${1}"
}

t_value() {
  eval "echo \"\$${1}\""
}

update_caminfo() {
  # Debug flag
  debug=$(fw_printenv -n debug); [ -z "$debug" ] && debug="0"

  _tmpfile=${ui_tmp_dir}/sysinfo.tmp
  :>$_tmpfile
  # add all web-related config files
  # do not include bigbro, ntp
  for _f in admin email ftp motion socks5 telegram yadisk yucca; do
    [ -f "${ui_config_dir}/${_f}.conf" ] && cat "${ui_config_dir}/${_f}.conf" >>$_tmpfile
  done; unset _f

  # Hardware
  flash_size=$(awk '{sum+=sprintf("0x%s", $2);} END{print sum/1048576;}' /proc/mtd)
  sensor=$(ipcinfo --short-sensor)
  sensor_ini=$(ipcinfo --long-sensor)
  soc=$(ipcinfo --chip-name)
  soc_family=$(ipcinfo --family)

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
  ui_password=$(grep admin /etc/httpd.conf|cut -d: -f3)
  ui_password_fw=$(grep admin /rom/etc/httpd.conf|cut -d: -f3)

  # Network
  network_dhcp="false"; [ "$(cat /etc/network/interfaces | grep "eth0 inet" | grep dhcp)" ] && network_dhcp="true"
  if [ -f /etc/resolv.conf ]; then
    network_dns_1=$(cat /etc/resolv.conf | grep nameserver | sed -n 1p | cut -d' ' -f2)
    network_dns_2=$(cat /etc/resolv.conf | grep nameserver | sed -n 2p | cut -d' ' -f2)
  fi

  # if gateway is not set then no default route nor wan mac present
  _default_route="$(ip r | grep ^default)"
  if [ -n "$_default_route" ]; then
    _default_iface=$(echo "$_default_route" | awk '{print $5}')
    network_wan_mac=$(cat /sys/class/net/${_default_iface}/address)
    network_gateway=$(echo "$_default_route" | awk '{print $3}')
  fi; unset _default_route;unset _default_iface

  network_hostname=$(hostname -s)
  network_interfaces=$(/sbin/ifconfig | grep '^\w' | awk {'print $1'} | tr '\n' ' ' | sed 's/ $//' )
  network_address=$(printenv | grep HTTP_HOST | cut -d= -f2 | cut -d: -f1)
  # FIXME: multiple interfaces give multiple addresses
  network_macaddr=$(ifconfig -a | grep HWaddr | sed s/.*HWaddr// | sed "s/ //g" | uniq | tail -1)
  network_netmask=$(ifconfig eth0 | grep "inet " | cut -d: -f4)

  overlay_root=$(mount | grep upperdir= | sed -r 's/^.*upperdir=([a-z\/]+).+$/\1/')

  # Default timezone is GMT
  tz_data=$(cat /etc/TZ)
  tz_name=$(cat /etc/tz_name)
  if [ -z "$tz_data" ] || [ -z "$tz_name" ]; then
    tz_data="GMT0"; echo "$tz_data" >/etc/TZ
    tz_name="Etc/GMT"; echo "$tz_name" >/etc/tz_name
  fi

  echo "flash_size=\"$flash_size\"
fw_version=\"$fw_version\"
fw_variant=\"$fw_variant\"
fw_build=\"$fw_build\"
network_address=\"$network_address\"
network_dhcp=\"$network_dhcp\"
network_dns_1=\"$network_dns_1\"
network_dns_2=\"$network_dns_2\"
network_gateway=\"$network_gateway\"
network_hostname=\"$network_hostname\"
network_interfaces=\"$network_interfaces\"
network_macaddr=\"$network_macaddr\"
network_netmask=\"$network_netmask\"
network_wan_mac=\"$network_wan_mac\"
overlay_root=\"$overlay_root\"
mj_version=\"$mj_version\"
soc=\"$soc\"
soc_family=\"$soc_family\"
soc_has_temp=\"$soc_has_temp\"
sensor=\"$sensor\"
sensor_ini=\"$sensor_ini\"
tz_data=\"$tz_data\"
tz_name=\"$tz_name\"
ui_password=\"$ui_password\"
ui_password_fw=\"$ui_password_fw\"
ui_version=\"$ui_version\"
" >>$_tmpfile

  # sort content alphabetically
  sort <$_tmpfile | sed /^$/d >$sysinfo_file && rm $_tmpfile && unset _tmpfile

  echo -e "debug=\"$debug\"\n# caminfo $(date +"%F %T")\n" >>$sysinfo_file
}

xl() {
  _c="$1"
  echo "<b>${_c}</b>"
  _o=$($_c 2>&1)
  [ $? -ne 0 ] && error=1
  [ -n "$_o" ] && echo "<div class=\"x-small p-3\"><i>${_o}</i></div>"
  unset _c; unset _o
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
include /etc/webui/socks5.conf
include /etc/webui/telegram.conf
include /etc/webui/yadisk.conf

# reload_locale
# check_password
%>
