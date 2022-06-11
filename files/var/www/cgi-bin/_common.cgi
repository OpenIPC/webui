#!/usr/bin/haserl
<%in _html.cgi %>
<%in _bootstrap.cgi %>
<%
beats() {
  echo -n "@$(echo "$(date -u -d "1970-01-01 $(TZ=UTC-1 date +%T)" +%s) * 10 / 864" | bc)"
}

check_password() {
  uri1=/cgi-bin/webui-settings.cgi
  uri2=/cgi-bin/webui-settings-update.cgi
  [ -z "$REQUEST_URI" ] && return
  [ "$REQUEST_URI" = "$uri1" ] && return
  [ "$REQUEST_URI" = "$uri2" ] && return

  password=$(awk -F ':' '/cgi-bin/ {print $3}' /etc/httpd.conf)
  if [ "12345" = "$password" ]; then
    flash_save "danger" "$tMsgSetYourOwnPassword"
    redirect_to "$uri1"
  fi
}

ex() {
  h6 "# ${1}"
  report_log "$(eval $1 2>&1)"
}

flash_append() {
  echo "$1:$2" >> /tmp/webui-flash.txt
}

flash_delete() {
  :> /tmp/webui-flash.txt
}

flash_read() {
  [ ! -f /tmp/webui-flash.txt ] && return
  flash=$(cat /tmp/webui-flash.txt)
  [ -z "$flash" ] && return
  type=$(echo $flash | cut -d ":" -f 1)
  message=$(echo $flash | cut -d ":" -f 2)
  echo "<div class=\"alert alert-${type} alert-dismissible fade show\" role=\"alert\">${message} <button type=\"button\" class=\"btn-close\" data-bs-dismiss=\"alert\" aria-label=\"Close\"></button></div>"
  flash_delete
}

flash_save() {
  xheader="X-ErrorMessage: $2"
  echo "$1:$2" > /tmp/webui-flash.txt
}

get_firmware_info() {
  if [ ! -f /tmp/fwinfo.txt ]; then
    fw_version=$(cat /etc/os-release | grep "OPENIPC_VERSION" | cut -d= -f2 | tr -d /\"/)
    fw_variant=$(cat /etc/os-release | grep "BUILD_OPTION" | cut -d= -f2 | tr -d /\"/)
    [ -z "$fw_variant" ] && fw_variant="lite"
    fw_build=$(cat /etc/os-release | grep "GITHUB_VERSION" | cut -d= -f2 | tr -d /\"/)
    echo -e "$fw_version\n$fw_variant\n$fw_build" > /tmp/fwinfo.txt
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

source $PWD/_settings.sh
source $PWD/locale/en.sh
locale=$(cat /etc/web_locale)
[ -z "$locale" ] && locale="en"
[ "$locale" != "en" -a -f "$PWD/locale/$locale.sh" ] && source $PWD/locale/${locale}.sh

check_password
%>
