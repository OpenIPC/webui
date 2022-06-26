#!/usr/bin/haserl
<%
# tag "tag" "text" "css" "extras"
tag() {
  _tag="$1"; _txt="$2"; _css="$3"; _xtr="$4"
  [ -n "$_css" ] && _css=" class=\"${_css}\""
  [ -n "$_xtr" ] && _xtr=" ${_xtr}"
  echo "<${_tag}${_css}${_xtr}>${_txt}</${_tag}>"
  unset _tag; unset _txt; unset _css; unset _xtr
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

pre_() { A "pre" "$1" "$2"; }
_pre() { Z "pre"; }

span_() { A "span" "$1" "$2"; }
_span() { Z "span"; }

# alert_ "type" "extras"
alert_() {
  div_ "alert alert-${1}" "$2"
}

_alert() {
  _div
}

# alert "text" "type" "extras"
alert() {
  alert_ "$2" "$3"
  echo "$1"
  _alert
}

beats() {
  echo "@$(echo "$(date -u -d "1970-01-01 $(TZ=UTC-1 date +%T)" +%s)*10/864"|bc)"
}

# button_link_to "text" "url" "type" "extras"
button_link_to() {
  echo "<a class=\"btn btn-${3}\" href=\"${2}\" ${4}>${1}</a>"
}

button_home() {
  echo "<a class=\"btn btn-primary\" href=\"/\">$t_b_home</a>"
}

button_reboot() {
  button_link_to "$t_b_reboot" "/cgi-bin/reboot.cgi" "danger"
}

# button_refresh
button_refresh() {
  link_to "$t_b_refresh" "#" "btn btn-primary refresh"
}

# button_submit "text" "type" "extras"
button_submit() {
  _t="$1"; [ -z "$_t" ] && _t="$t_btn_submit"
  _c="$2"; [ -z "$_c" ] && _c="primary"
  _x="$3"; [ -z "$_x" ] && _x=" ${_x}"
  echo "<p class=\"button submit mt-2\"><input type=\"submit\" class=\"btn btn-${_c}\"${_x} value=\"${_t}\"></p>"
  unset _c; unset _t; unset _x
}

check_for_lock() {
  [ -f /tmp/webjob.lock ] && redirect_back "danger" "Another progress is running."
  touch /tmp/webjob.lock
}

#check_password() {
#  [ "0${debug}" -ge "1" ] && return
#  [ -z "$REQUEST_URI" ] || [ "$REQUEST_URI" = "/cgi-bin/webui-settings.cgi" ] && return
#  if [ -z "$password" ] || [ "$password_fw" = "$password" ]; then
#    redirect_to "/cgi-bin/webui-settings.cgi" "danger" "$t_wui_a"
#  fi
#}

e() {
  echo -e -n "$1"
}

ex() {
  # NB! $() forks process and stalls output.
  h4 "# ${1}"
  pre_ "small"
  eval "$1" | sed "s/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g;s/\"/\&quot;/g" 2>&1
  _pre
}

field_() {
  echo "<p class=\"$1\">"
}

_field() {
  echo "</p>"
}

# field_checkbox "name" "extras"
field_checkbox() {
  field_ "boolean form-check"
    echo "<input type=\"hidden\" name=\"${1}\" id=\"${1}-false\" value=\"false\">"
    echo "<input type=\"checkbox\" name=\"${1}\" id=\"${1}\" $(t_checked "$1" "true") value=\"true\" class=\"form-check-input\" ${2}>"
    label "$1" "$2"
  _field
}

# field_file "name"
field_file() {
  field_ "file"
    label "$1"
    input "file" "$1" "$2"
    help "$1"
  _field
}

# field_hidden "name"
field_hidden() {
  input "hidden" "$1" "hidden"
}

# field_number "name"
field_number() {
  field_ "number"
    label "$1"
    input "text" "$1" "form-control text-end"
    help "$1"
  _field
}

# field_password "name"
field_password() {
  field_ "password"
    label "$1"
    echo "<span class=\"input-group\">"
      input "password" "$1"
      echo "<label class=\"input-group-text\"><input class=\"form-check-input me-1\" type=\"checkbox\" data-for=\"${1}\">  show</label>"
      echo "</span>"
    help "$1"
  _field
}

# field_range "name"
field_range() {
  field_ "range"
    label "$1"
    echo "<span class=\"input-group\">"
    if [ -n "$(t_options "$1" | grep -E auto)" ]; then
      echo "<label class=\"input-group-text\">auto <input class=\"form-check-input auto-value ms-1\" type=\"checkbox\" data-for=\"${1}\" data-value=\"$(t_default "$1")\" $(t_checked "$1" "auto")></label>"
    fi
    echo "<input type=\"range\" name=\"${1}\" id=\"${1}\" class=\"form-control form-range\" value=\"$(t_value "$1")\">"
    echo "<span class=\"input-group-text\"><span id=\"${1}-value\" class=\"text-end\">$(t_value "$1")</span></span>"
    echo "</span>"
    help "$1"
  _field
}

# field_select "name"
field_select() {
  field_ "select"
    label "$1"
    echo "<select class=\"form-select\" id=\"${1}\" name=\"${1}\">"
    [ -z "$(t_value "$1")" ] && echo "<option value=\"\">Select from available options</option>"
    for o in $(t_options "$1"); do
      _v="${o%|*}"; _n="${o#*|}"; [ "$1" != "mj_isp_sensorConfig" ] && _n=${_n//_/ }
      echo "<option value=\"${_v}\" $(t_selected "$1" "${_v}")>${_n}</option>"
      unset _v; unset _n
    done
    echo "</select>"
    units "$1"
    help "$1"
  _field
}

# field_swith "name"
field_switch() {
  field_ "boolean"
    echo "<span class=\"form-check form-switch\">"
      input "switch" "$1"
      label "$1" "form-check-label"
    echo "</span>"
    help "$1"
  _field
}

# field_text "name" "classes" "extras"
field_text() {
  field_ "string"
    label "$1"
    input "text" "$1" "$2" "$3"
    help "$1"
  _field
}

field_textarea() {
  field_ "text"
    label "$1"
    input "textarea" "$1"
    help "$1"
  _field
}

flash_append() {
  echo "$1:$2" >> "$flash_file"
}

flash_delete() {
  :> "$flash_file"
}

flash_read() {
  [ ! -f "$flash_file" ] && return
  flash=$(cat "$flash_file")
  [ -z "$flash" ] && return
  alert_ "$(echo $flash | cut -d':' -f1) alert-dismissible fade show" "role=\"alert\""
    echo "$(echo $flash | cut -d':' -f2)"
    echo "<button type=\"button\" class=\"btn btn-close\" data-bs-dismiss=\"alert\" aria-label=\"Close\"></button>"
   _alert
  flash_delete
}

flash_save() {
  echo "${1}:${2}" > $flash_file
}

form_() {
  _m="$2"
  [ -z "$_m" ] && _m="post"

  A "form" "" "action=\"${1}\" method=\"${_m}\" ${3}"
  unset _m
}

_form() {
  Z "form"
}

form_upload_() {
  echo "<form action=\"$1\" method=\"post\" enctype=\"multipart/form-data\">"
}

get_soc_temp() {
  soc_temp=$(ipcinfo --temp)
}

header_ok() {
  echo "HTTP/1.1 200 OK
Content-type: application/json; charset=UTF-8
Cache-Control: no-store
Pragma: no-cache
Date: $(TZ=GMT0 date +'%a, %d %b %Y %T %Z')
Server: $SERVER_SOFTWARE

{}"
}

help() {
  [ -z "$(t_hint "$1")" ] && return
  echo "<span class=\"hint text-secondary\">$(t_hint "$1")</span>"
}

html_title() {
  [ -n "$1" ] && echo -n "$1 - "
  echo -n "OpenIPC"
}

# image "src" "classes" "extras"
image() {
  echo -n "<img src=\"${1}\" alt=\"Image: ${1}\" class=\"${2}\" ${3}>"
}

# input "type" "name" "classes" "value" "extras"
input() {
  # input type
  _t="$1"

  # input name
  _n="$2"

  # css class
  _c="form-control"

  # extra css class
  _c2="$3"

  # placeholder
  eval _p=\$sP_${_n}
  [ -n "$_p" ] && _p=" placeholder=\"${_p}\""

  #  value
  _v="$(t_value "$_n")"

  # extra attributes
  _x2="$4"

  case "$1" in
  checkbox)
    _c="form-check-input"
    _v="true"
    _x="$(t_checked "$_n" "$_v")"
    echo "<input type=\"hidden\" name=\"${_n}\" id=\"${_n}-false\" value=\"false\">"
    ;;
  switch)
    _t="checkbox"
    _c="form-check-input"
    _v="true"
    _x="role=\"switch\""; [ -n "$(t_checked "$2" "$_v")" ] && _x="$_x $(t_checked "$2" "$_v")"
    echo "<input type=\"hidden\" name=\"${_n}\" id=\"${_n}-false\" value=\"false\">"
    ;;
  text)
    ;;
  textarea)
    ;;
  range)
    _c="${_c} form-range"
    _o="$(t_options "$_n")"
    _x="$(t_disabled "$_n" "auto") data-units=\"$(t_units "$_n")\""
    ;;
  *)
    ;;
  esac

  [ -n "$_c2" ] && _c="${_c} ${_c2}"; [ -n "$_c" ] && _c=" class=\"${_c}\""
  [ -n "$_x2" ] && _x="${_x} ${_x2}"; [ -n "$_x" ] && _x=" ${_x}"

  if [ "textarea" = "$1" ]; then
    echo "<textarea id=\"${_n}\" name=\"${_n}\"${_c}${_x}>${_v}</textarea>"
  else
    [ -n "$_v" ] && _v=" value=\"${_v}\""
    echo "<input type=\"${_t}\" id=\"${_n}\" name=\"${_n}\"${_v}${_c}${_p}${_x}>"
  fi
  unset _c; unset _c2; unset _n; unset _o; unset _p; unset _t; unset _v; unset _x; unset _x2
}

# label "name" "classes" "extras"
label() {
  _c="form-label"; [ -n "$2" ] && _c="${_c} ${2}"
  _l="$(t_label "$1")"; [ -z "$_l" ] && _l="$1" && _c="${_c} bg-warning"
  _u=$(t_units "$1"); [ -n "$_u" ] && _l="${_l}, <span class=\"units text-secondary x-small\">$_u</span>"
  _x="$3"; [ -n "$_x" ] && _x=" ${_x}"
  echo "<label for=\"${1}\" class=\"${_c}\"${_x}>${_l}</label>"
  unset _c; unset _l; unset _u; unset _x
}

link_to() {
  echo "<a href=\"${2}\" class=\"${3}\" ${4}>${1}</a>"
}

# pre "text" "classes" "extras"
pre() {
  # replace <, >, &, ", and ' with HTML entities
  tag "pre" "$(echo -e "$1" | sed "s/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g;s/\"/\&quot;/g")" "$2" "$3"
}

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
Date: $(TZ=GMT0 date +'%a, %d %b %Y %T %Z')
Location: $1
Server: $SERVER_SOFTWARE
Status: 302 Moved Temporarily
"
  exit 0
}

reload_locale() {
  _l="$(cat /etc/web_locale)"
  if [ -f "/var/www/lang/${_l}.sh" ]; then
    source "/var/www/lang/${_l}.sh"
    locale="$_l"
  else
    locale="en"
  fi
  unset _l
}

report_error() {
  h4 "$tMsgSomethingHappened" "text-danger"
  alert "$1" "danger"
}

report_info() {
  alert "$1" "info"
}

# report_log "text" "extras"
report_log() {
  pre "$1" "small" "$2"
}

report_command_error() {
  h2 "$tMsgSomethingHappened" "text-danger"
  alert_ "danger"
  report_command_info "$1" "$2"
  _alert
}

report_command_info() {
  h4 "# $1"
  report_log "$2"
}

report_command_success() {
  h2 "$tMsgCommandExecuted" "success"
  report_command_info "$1" "$2"
}

# row_ "class"
row_() {
  div_ "row ${1}" "$2"
}

_row() {
  _div
}

row() {
  row_ "$2"
  echo "$1"
  _row
}

sanitize() {
  z="$1"
  eval $z=$(eval echo \$$z | sed s/^\\/// | sed s/\\/$//)
  unset z
}

signature() {
  _f=/tmp/webui-signature.txt
  if [ ! -f "$_f" ]; then
    echo "${soc} (${soc_family} family), $sensor, ${flash_size} MB Flash. ${fw_version}-${fw_variant}. ${hostname}, ${wan_mac}" > $_f
  fi
  cat $_f
  unset _f
}

t_checked() {
  [ "$2" = "$(t_value "$1")" ] && echo "checked"
}

t_default() {
  eval "echo \$tDefault_${1}"
}

t_disabled() {
  [ "$2" = "$(t_value "$1")" ] && echo "disabled"
}

t_hint() {
  eval "echo \$tH_${1}"
}

t_label() {
  eval "echo \$tL_${1}"
}

t_options() {
  eval "echo \${tOptions_${1}//,/ }"
}

t_readonly() {
  [ "$2" = "$(t_value "$1")" ] && echo -n "readonly"
}

t_selected() {
  [ "$2" = "$(t_value "$1")" ] && echo -n "selected"
}

t_units() {
  eval "echo \$tUnits_${1}"
}

t_value() {
  eval "echo \"\$$1\""
}

units() {
  [ -n "$(t_units "$1")" ] && span "$(t_units "$1")" "input-group-text"
}

update_caminfo() {
  # Debug flag
  debug=$(fw_printenv -n debug); [ -z "$debug" ] && debug="0"

  # Hardware
  flash_size=$(awk '{sum+=sprintf("0x%s", $2);} END{print sum/1048576;}' /proc/mtd)
  sensor=$(ipcinfo --short-sensor)
  sensor_ini=$(ipcinfo --long-sensor)
  soc=$(ipcinfo --chip-name)
  soc_family=$(ipcinfo --family)

  # Firmware
  fw_version=$(grep "OPENIPC_VERSION" /etc/os-release | cut -d= -f2 | tr -d /\"/)
  fw_variant=$(grep "BUILD_OPTION" /etc/os-release | cut -d= -f2 | tr -d /\"/); [ -z "$fw_variant" ] && fw_variant="lite"
  fw_build=$(grep "GITHUB_VERSION" /etc/os-release | cut -d= -f2 | tr -d /\"/)
  mj_version=$($mj_bin_file -v)

  # WebUI version
  ui_version="bundled"; [ -f /var/www/.version ] && ui_version=$(cat /var/www/.version)
  password=$(grep admin /etc/httpd.conf|cut -d: -f3)
  password_fw=$(grep admin /rom/etc/httpd.conf|cut -d: -f3)

  # Network
  dhcp="false"; [ "$(cat /etc/network/interfaces | grep "eth0 inet" | grep dhcp)" ] && dhcp="true"
  dns_1=$(cat /etc/resolv.conf | grep nameserver | sed -n 1p | cut -d' ' -f2)
  dns_2=$(cat /etc/resolv.conf | grep nameserver | sed -n 2p | cut -d' ' -f2)
  gateway=$(ip r | grep default | cut -d' ' -f3)
  hostname=$(hostname -s)
  interfaces=$(/sbin/ifconfig | grep '^\w' | awk {'print $1'} | tr '\n' ' ' | sed 's/ $//' )
  ipaddr=$(printenv | grep HTTP_HOST | cut -d= -f2 | cut -d: -f1)
  macaddr=$(ifconfig -a | grep HWaddr | sed s/.*HWaddr// | sed "s/ //g" | uniq)
  netmask=$(ifconfig eth0 | grep "inet " | cut -d: -f4)
  wan_mac=$(cat /sys/class/net/$(ip r | awk '/default/ {print $5}')/address)

  # Default timezone is GMT
  tz_data=$(cat /etc/TZ)
  tz_name=$(cat /etc/tz_name)
  if [ -z "$tz_data" ] || [ -z "$tz_name" ]; then
    tz_data="GMT0"; echo "$tz_data" > /etc/TZ
    tz_name="Etc/GMT"; echo "$tz_name" > /etc/tz_name
  fi

  echo "# caminfo $(date +"%F %T")
debug=\"$debug\"
dhcp=\"$dhcp\"
dns_1=\"$dns_1\"
dns_2=\"$dns_2\"
flash_size=\"$flash_size\"
fw_version=\"$fw_version\"
fw_variant=\"$fw_variant\"
fw_build=\"$fw_build\"
gateway=\"$gateway\"
hostname=\"$hostname\"
interfaces=\"$interfaces\"
ipaddr=\"$ipaddr\"
macaddr=\"$macaddr\"
mj_version=\"$mj_version\"
netmask=\"$netmask\"
password=\"$password\"
password_fw=\"$password_fw\"
soc=\"$soc\"
soc_family=\"$soc_family\"
sensor=\"$sensor\"
sensor_ini=\"$sensor_ini\"
tz_data=\"$tz_data\"
tz_name=\"$tz_name\"
ui_version=\"$ui_version\"
wan_mac=\"$wan_mac\"
# end " > $sysinfo_file
}

xl() {
  _c="$1"
  echo "<b>${_c}</b>"
  _o=$($_c 2>&1)
  [ $? -ne 0 ] && error=1
  [ -n "$_o" ] && echo "<div class=\"x-small p-3\"><i>${_o}</i></div>"
  unset _c; unset _o
}


dump() {
  echo "Content-Type: text/plain; charset=UTF-8
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
  source "$i"
}

load_plugins() {
  for i in $(ls -1 plugin-*); do
    eval "$(grep 'plugin_name=' $i)"
    echo "<li><a class=\"dropdown-item\" href=\"/cgi-bin/${i}\">${plugin_name}</a></li>"
    unset plugin_name
  done
}

log() {
  echo $1 >/tmp/webui.log
}

mj_bin_file=/usr/bin/majestic
flash_file=/tmp/webui-flash.txt
sysinfo_file=/tmp/sysinfo.txt

config_path=/etc/webui
[ ! -d $config_path ] && mkdir -p $config_path

lang_path=/var/www/lang/
[ ! -d $lang_path ] && mkdir -p $lang_path

[ ! -f $sysinfo_file ] && update_caminfo
source $sysinfo_file

pagename=$(basename "$SCRIPT_NAME")
pagename="${pagename%%.*}"

source p/settings.sh
source p/locale_en.sh

reload_locale
# check_password
%>
