#!/usr/bin/haserl
<%
print2c() {
  # printf "%-24s|%16s|\n" "${1}" "${2}"
  echo -en "<span class=\"title\">$1</span><span>$2</span>\n"
}
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
debug_message() {
  # [ "$HTTP_MODE" = "development" ] &&
  echo "$(date +"%F %T") $1" >> /tmp/webui.log
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
flash_append() {
  echo "$1:$2" >> /tmp/webui-flash.txt
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
  soc_temp=$(ipcinfo --temp)
}
get_http_time() {
  http_time=$(TZ=GMT date +"%a, %d %b %Y %T %Z")
}
get_software_info() {
  mj_bin_file="/usr/bin/majestic"
  mj_version=$(${mj_bin_file} -v)
  ui_version=$(cat /var/www/.version)
}
get_system_info() {
  hostname=$(hostname -s)
  interfaces=$(/sbin/ifconfig | grep '^\w' | awk {'print $1'})
  ipaddr=$(printenv | grep HTTP_HOST | cut -d= -f2 | cut -d: -f1)
  macaddr=$(ifconfig -a | grep HWaddr | sed s/.*HWaddr// | uniq)
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
   [ ! -z "$1" ] && echo -n "$1 - "
  echo -n  "OpenIPC"
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
  echo "<h2 class=\"text-danger\">$tMsgSomethingHappened</h2><div class=\"alert alert-danger mb-3\">$1</div>"
}
report_info() {
  echo "<div class=\"alert alert-info mb-3\">$1</div>"
}
report_log() {
  echo -e "<pre class=\"bg-light p-3\">$1</pre>"
}
report_warning() {
  echo "<div class=\"alert alert-warning mb-3\">$1</div>"
}
report_command_error() {
  echo "<h2 class=\"text-danger\">$tMsgSomethingHappened</h2><div class=\"alert alert-danger mb-3\"><b># $1</b><pre class=\"mb-0\">$2</pre></div>"
}
report_command_info() {
  echo "<div class=\"alert alert-info mb-3\"><b># $1</b><pre class=\"mb-0\">$2</pre></div>"
}
report_command_success() {
  echo "<h2 class=\"text-success\">$tMsgCommandExecuted</h2><div class=\"alert alert-success mb-3\"><b># $1</b><pre class=\"mb-0\">$2</pre></div>"
}

source $PWD/locale/en.sh
locale=$(cat /etc/web_locale)
[ -z "$locale" ] && locale="en"
[ "$locale" != "en" -a -f "$PWD/locale/$locale.sh" ] && source $PWD/locale/${locale}.sh

check_password
%>
