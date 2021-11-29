#!/usr/bin/haserl
content-type: text/html

<%in _header.cgi %>
<h1>Updating Majestic settings</h1>
<pre>
<%
data=$(printenv|grep FORM_)
for name in $data; do
  key=".$(echo $name | sed 's/^FORM_//' | cut -d= -f1 | sed 's/_/./g')"
  value=$(echo $name | cut -d= -f2)
  if [ "${value}" ]; then
    echo "yaml-cli -s \"$key\" \"$value\"" | logger -t microbe-web
    yaml-cli -s "$key" "$value"
  fi
  if [ -z "${value}" ]; then
    echo "yaml-cli -d \"$key\"" | logger -t microbe-web
    yaml-cli -d "$key"
  fi
done
killall -1 majestic
%>
</pre>
<script>setTimeout('window.location="/cgi-bin/majestic.cgi"',3000);</script>
<%in _footer.cgi %>
