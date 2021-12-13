<%
check_password() {
  uri1=/cgi-bin/webui-password.cgi
  uri2=/cgi-bin/webui-password-update.cgi
  [ -z "$REQUEST_URI" ] && return
  [ "$REQUEST_URI" = "$uri1" ] && return
  [ "$REQUEST_URI" = "$uri2" ] && return

  password=$(awk -F ':' '/cgi-bin/ {print $3}' /etc/httpd.conf)
  if [ "$password" = "12345" ]; then
    flash_save "danger" "You must set your own secure password!"
    redirect_to "$uri1"
  fi
}
html_title() {
   [ ! -z "$1" ] && echo -n "$1 - "
  echo -n  "OpenIPC"
}
http_header_connection_close() {
  echo "Connection: close"
}
http_header_html() {
  echo "Content-Type: text/html; charset=UTF-8"
}
http_header_nocache() {
  echo "Pragma: no-cache"
}
http_header_text() {
  echo "Content-Type: text/plain; charset=UTF-8"
}
redirect_to() {
  echo "HTTP/1.1 302 Moved Temporarily"
  echo "Content-type: text/html; charset=UTF-8"
  echo "Date: $(TZ=GMT date +"%a, %d %b %Y %T %Z")"
  echo "Location: $1"
  echo "Server: httpd"
  echo "Status: 302 Moved Temporarily"
  echo ""
}
report_error() {
  echo "<h2 class=\"text-danger\">Oops. Something happened.</h2>"
  echo "<div class=\"alert alert-danger mb-3\">$1</div>"
}
report_info() {
  echo "<div class=\"alert alert-info mb-3\">$1</div>"
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
flash_delete() {
  :> /tmp/webui-flash.txt
}
flash_read() {
  flash=$(cat /tmp/webui-flash.txt)
  [ -z "$flash" ] && return
  type=$(echo $flash | cut -d ":" -f 1)
  message=$(echo $flash | cut -d ":" -f 2)
  echo "<div class=\"alert alert-$type\">$message</div>"
  flash_delete
}
flash_save() {
  xheader="X-ErrorMessage: $2"
  echo "$1:$2" > /tmp/webui-flash.txt
}

check_password
%>
