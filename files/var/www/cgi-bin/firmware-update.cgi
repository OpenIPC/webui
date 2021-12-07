#!/usr/bin/haserl
<%
[ -z "$FORM_reset" ] && command="sysupgrade" || command="sysupgrade -n"
output=$($command 2>&1)
result=$?
if [ "0" -ne "$result" ]; then %>
<%in _header.cgi %>
<h2 class="text-danger">Oops. Something happened.</h2>
<div class="alert alert-danger">
<pre>
<b># <%= $command %></b>
<%= "$output" %></pre>
</div>
<%in _footer.cgi %>
<% else
  echo "HTTP/1.1 302 Moved Temporarily"
  echo "Content-type: text/html; charset=UTF-8"
  echo "Date: $(TZ=GMT date +"%a, %d %b %Y %T %Z")"
  echo "Location: /cgi-bin/updates.cgi"
  echo "Server: httpd"
  echo "Status: 302 Moved Temporarily"
fi
%>
