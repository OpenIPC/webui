#!/usr/bin/haserl
content-type: text/html

<%in _header.cgi %>
<h2>Updating Majestic settings</h2>
<%
data="$(printenv|grep FORM_)"
IFS=$'\n' # make newlines the only separator
for name in $data; do
  key=".$(echo $name | sed 's/^FORM_//' | cut -d= -f1 | sed 's/-/./g')"
  value="$(echo $name | cut -d= -f2)"
  oldvalue=$(yaml-cli -g "$key")

  if [ "$key" = ".image.rotate" ]; then
    if [ "$value" = "0°" ]; then
      value="none"
    else
      value=${value//°/}
    fi
  fi

  if [ -z "$value" ]
  then
    if [ -z "$oldvalue" ]
    then
      echo "<div class=\"alert alert-warning mb-3\">"
      echo "Empty value for ${key}. Existing value is empty, too. Skipping."
      echo "</div>"
    else
      echo "<div class=\"alert alert-danger mb-3\">"
      echo "Empty value for ${key}. Existing value is '${oldvalue}'. Deleting."
      echo "<br><b># yaml-cli -d \"$key\"</b>"
      echo "</div>"
      yaml-cli -d "$key"
    fi
  else
    if [ "$oldvalue" = "$value" ]
    then
      echo "<div class=\"alert alert-warning mb-3\">"
      echo "Same value for ${key}. Skipping."
      echo "</div>"
    else
      echo "<div class=\"alert alert-info mb-3\">"
      echo "Updated value for ${key}. Existing value is '${oldvalue}'. Saving."
      echo "<br><b># yaml-cli -s \"$key\" \"$value\"</b>"
      echo "</div>"
      yaml-cli -s "$key" "$value"
    fi
  fi
done
%>

<p><a href="/cgi-bin/majestic.cgi">Go back to Majestic settings page.</a></p>

<%in _footer.cgi %>

<% killall -1 majestic %>
