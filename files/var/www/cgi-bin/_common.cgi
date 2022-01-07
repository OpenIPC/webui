<%
beats() {
  echo -n "@$(echo "$(date -u -d "1970-01-01 $(TZ=UTC-1 date +%T)" +%s) * 10 / 864" | bc)"
}
check_password() {
  uri1=/cgi-bin/webui-password.cgi
  uri2=/cgi-bin/webui-password-update.cgi
  [ -z "$REQUEST_URI" ] && return
  [ "$REQUEST_URI" = "$uri1" ] && return
  [ "$REQUEST_URI" = "$uri2" ] && return

  password=$(awk -F ':' '/cgi-bin/ {print $3}' /etc/httpd.conf)
  if [ "12345" = "$password" ]; then
    flash_save "danger" "You must set your own secure password!"
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
  echo "<div class=\"alert alert-${type} alert-dismissible fade show\" role=\"alert\">${message}"
  echo "<button type=\"button\" class=\"btn-close\" data-bs-dismiss=\"alert\" aria-label=\"Close\"></button>"
  echo "</div>"
  flash_delete
}
flash_save() {
  xheader="X-ErrorMessage: $2"
  echo "$1:$2" > /tmp/webui-flash.txt
}
get_soc() {
  soc=$(ipcinfo --chip_id 2>&1)
  case "$soc" in
    gk7605v100 | gk7205v300 | gk7202v300 | gk7205v200)
      soc_sdk="gk7205v200"
      ;;
    hi3516dv100 | hi3516av100)
      soc_sdk="hi3516av100"
      ;;
    hi3518cv200 | hi3518ev200 | hi3518ev201 | hi3516cv200)
      soc_sdk="hi3516cv200"
      ;;
    hi3516ev100 | hi3516cv300)
      soc_sdk="hi3516cv300"
      ;;
    hi3516dv300 | hi3516av300 | hi3516cv500)
      soc_sdk="hi3516cv500"
      ;;
    hi3516ev200 | hi3518ev300 | hi3516dv200 | hi3516ev300)
      soc_sdk="hi3516ev300"
      ;;
    nt98562 | nt98566)
      soc_sdk="nt9856x"
      ;;
    ssc337 | ssc335)
      soc_sdk="ssc335"
      ;;
    xm530 | xm550)
      soc_sdk="xm550"
      ;;
    *)
      soc_sdk=
      ;;
  esac
}
html_title() {
   [ ! -z "$1" ] && echo -n "$1 - "
  echo -n  "OpenIPC"
}
redirect_to() {
  echo "HTTP/1.1 302 Moved Temporarily"
  echo "Content-type: text/html; charset=UTF-8"
  echo "Date: $(TZ=GMT date +"%a, %d %b %Y %T %Z")"
  echo "Location: $1"
  echo "Server: httpd"
  echo "Status: 302 Moved Temporarily"
  echo "$xheader"
  echo ""
}
report_error() {
  echo "<h2 class=\"text-danger\">Oops. Something happened.</h2>"
  echo "<div class=\"alert alert-danger mb-3\">$1</div>"
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
  echo "<h2 class=\"text-danger\">Oops. Something happened.</h2>"
  echo "<div class=\"alert alert-danger mb-3\">"
  echo "<b># $1</b>"
  echo "<pre class=\"mb-0\">$2</pre>"
  echo "</div>"
}
report_command_info() {
  echo "<div class=\"alert alert-info mb-3\">"
  echo "<b># $1</b>"
  echo "<pre class=\"mb-0\">$2</pre>"
  echo "</div>"
}
report_command_success() {
  echo "<h2 class=\"text-success\">Command executed.</h2>"
  echo "<div class=\"alert alert-success mb-3\">"
  echo "<b># $1</b>"
  echo "<pre class=\"mb-0\">$2</pre>"
  echo "</div>"
}
check_password
%>
