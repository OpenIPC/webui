<%
redirect_to() {
  echo "HTTP/1.1 302 Moved Temporarily"
  echo "Content-type: text/html; charset=UTF-8"
  echo "Date: $(TZ=GMT date +"%a, %d %b %Y %T %Z")"
  echo "Location: $1"
  echo "Server: httpd"
  echo "Status: 302 Moved Temporarily"
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
%>
