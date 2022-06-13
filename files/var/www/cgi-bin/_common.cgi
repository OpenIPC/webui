#!/usr/bin/haserl
<%in _html.cgi %>
<%in _bootstrap.cgi %>
<%
beats() {
  echo -n "@$(echo "$(date -u -d "1970-01-01 $(TZ=UTC-1 date +%T)" +%s) * 10 / 864" | bc)"
}

check_password() {
  [ -z "$REQUEST_URI" ] && return
  [ "$REQUEST_URI" = "/cgi-bin/webui-settings.cgi" ] && return
  [ "$REQUEST_URI" = "/cgi-bin/webui-settings-update.cgi" ] && return

  default_password=$(grep admin /rom/etc/httpd.conf | cut -d: -f3)
  password=$(grep admin /etc/httpd.conf | cut -d: -f3)
  if [ "$default_password" = "$password" ]; then
    flash_save "danger" "$tMsgSetYourOwnPassword"
    redirect_to "/cgi-bin/webui-settings.cgi"
  fi
}

ex() {
  h6 "# ${1}"
  report_log "$(eval $1 2>&1)"
}

flash_file=/tmp/webui-flash.txt
flash_append() { echo "$1:$2" >> "$flash_file"; }
flash_delete() { :> "$flash_file"; }
flash_read() {
  [ ! -f "$flash_file" ] && return
  flash=$(cat "$flash_file")
  [ -z "$flash" ] && return
  alert_ "$(echo $flash | cut -d ":" -f 1) alert-dismissible fade show" "role=\"alert\""
    echo "$(echo $flash | cut -d ":" -f 2)"
    button "" "close" "data-bs-dismiss=\"alert\" aria-label=\"Close\""
   _alert
  flash_delete
}
flash_save() { echo "${1}:${2}" > "$flash_file"; }

get_firmware_info() {
  if [ ! -f /tmp/fwinfo.txt ]; then
    fw_version=$(cat /etc/os-release | grep "OPENIPC_VERSION" | cut -d= -f2 | tr -d /\"/)
    fw_variant=$(cat /etc/os-release | grep "BUILD_OPTION" | cut -d= -f2 | tr -d /\"/)
    fw_build=$(cat /etc/os-release | grep "GITHUB_VERSION" | cut -d= -f2 | tr -d /\"/)
    echo -e "$fw_version\n${fw_variant:=lite}\n$fw_build" > /tmp/fwinfo.txt
  else
    fw_version=$(sed -n 1p /tmp/fwinfo.txt)
    fw_variant=$(sed -n 2p /tmp/fwinfo.txt)
    fw_build=$(sed -n 3p /tmp/fwinfo.txt)
  fi
}

get_hardware_info() {
  if [ ! -f /tmp/hwinfo.txt ]; then
    soc=$(ipcinfo --chip-name)
    soc_family=$(ipcinfo --family)
    sensor=$(ipcinfo --short-sensor)
    sensor_ini=$(ipcinfo --long-sensor)
    flash_size=$(awk '{sum+=sprintf("0x%s", $2);} END{print sum/1048576;}' /proc/mtd)
    echo -e "$soc\n$soc_family\n$sensor\n$sensor_ini\n$flash_size" > /tmp/hwinfo.txt
  else
    soc=$(sed -n 1p /tmp/hwinfo.txt)
    soc_family=$(sed -n 2p /tmp/hwinfo.txt)
    sensor=$(sed -n 3p /tmp/hwinfo.txt)
    sensor_ini=$(sed -n 4p /tmp/hwinfo.txt)
    flash_size=$(sed -n 5p /tmp/hwinfo.txt)
  fi
}

get_http_time() {
  http_time=$(TZ=GMT date +"%a, %d %b %Y %T %Z")
}

get_soc_temp() {
  soc_temp=$(ipcinfo --temp)
}

get_software_info() {
  mj_bin_file="/usr/bin/majestic"
  mj_version=$(${mj_bin_file} -v)
  [ -f /var/www/.version ] && ui_version=$(cat /var/www/.version)
}

get_system_info() {
  hostname=$(hostname -s)
  interfaces=$(/sbin/ifconfig | grep '^\w' | awk {'print $1'})
  ipaddr=$(printenv | grep HTTP_HOST | cut -d= -f2 | cut -d: -f1)
  macaddr=$(ifconfig -a | grep HWaddr | sed s/.*HWaddr// | sed "s/ //g" | uniq)
  tz_data=$(cat /etc/TZ)
  [ -z "$tz_data" ] && tz_data="GMT0"
  [ ! -f /etc/tzname ] && $(grep "$tz_data" /var/www/js/tz.js | head -1 | cut -d ":" -f 2 | cut -d "," -f 1 | tr -d "'" > /etc/tzname)
  tz_name=$(cat /etc/tzname)
  wan_mac=$(cat /sys/class/net/$(ip r | awk '/default/ {print $5}')/address)
}

header_ok() {
  get_http_time
  echo "HTTP/1.1 200 OK
Content-type: application/json; charset=UTF-8
Cache-Control: no-store
Pragma: no-cache
Date: $http_time
Server: httpd

{}"
}

html_title() {
  [ -n "$1" ] && echo -n "$1 - "
  echo -n  "OpenIPC"
}

print2c() {
  echo "<span class=\"title\">${1}</span><span>${2}</span>"
}

redirect_to() {
  get_http_time
  echo "HTTP/1.1 302 Moved Temporarily
Content-type: text/html; charset=UTF-8
Cache-Control: no-store
Pragma: no-cache
Date: $http_time
Location: $1
Server: httpd
Status: 302 Moved Temporarily
$xheader
"
}

report_error() {
  echo "<h2 class=\"text-danger\">$tMsgSomethingHappened</h2>"
  alert "$1" "danger"
}

report_info() {
  alert "$1" "info"
}

# report_log "text" "extras"
report_log() {
  pre "$1" "class=\"small\" ${2}"
}

report_command_error() {
  echo "<h2 class=\"text-danger\">$tMsgSomethingHappened</h2>"
  alert_ "danger"
  b "# $1"
  pre "$2"
  _alert
}

report_command_info() {
  alert_ "info"
  b "# $1"
  pre "$2"
  _alert
}

report_command_success() {
  h2 "$tMsgCommandExecuted" "success"
  alert_ "success"
  p "# ${1}" "class=\"fw-bold\""
  pre "$2"
  _alert
}

t_default() {
  eval "echo \$tDefault_${1}"
}

t_label() {
  eval "echo \$tLabel_${1}"
}

t_checked() {
  [ "$2" = "$(t_value "$1")" ] && echo "checked"
}

t_hint() {
  eval "echo \$tHint_${1}"
}

t_placeholder() {
#  if [ "$1" = "isp_sensorConfig" ]; then
    eval "echo \$tPlaceholder_${1}"
#  else
#    eval "echo \${tPlaceholder_${1}//_/ }"
#  fi
}

t_readonly() {
  [ "$2" = "$(t_value "$1")" ] && echo "readonly"
}

t_selected() {
  [ "$2" = "$(t_value "$1")" ] && echo "selected"
}

t_options() {
  eval "echo \${tOptions_${1}//,/ }"
}

t_units() {
  eval "echo \$tUnits_${1}"
}

t_value() {
  eval "echo \$${1}"
}

reload_locale() {
  source $PWD/locale/${locale:=en}.sh
}

source $PWD/_settings.sh
source $PWD/locale/en.sh
locale=$(cat /etc/web_locale)
[ -z "$locale" ] && locale="en"
reload_locale
check_password
%>
