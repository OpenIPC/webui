#!/usr/bin/haserl
<%in _header.cgi %>
<h2>Updating Majestic settings</h2>
<%
cp -f /etc/majestic.yaml /tmp/majestic.yaml
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
  
  if [ "$key" = ".track" ]; then
    continue
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
      yaml-cli -d "$key" -i /tmp/majestic.yaml -o /tmp/majestic.yaml
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
      yaml-cli -s "$key" "$value" -i /tmp/majestic.yaml -o /tmp/majestic.yaml
    fi
  fi
done
 
settings_changed=$(diff -q /tmp/majestic.yaml /etc/majestic.yaml)
if [ ! -z "${settings_changed}" ];
then
  echo "<div class=\"alert alert-info mb-3\">"
  echo "Settings changed."
  echo "</div>"
  cp -f /tmp/majestic.yaml /etc/majestic.yaml
else
  echo "<div class=\"alert alert-warning mb-3\">"
  echo "Settings unchanged."
  echo "</div>"
fi
rm /tmp/majestic.yaml
%>

<p><a href="/cgi-bin/majestic.cgi">Go back to Majestic settings page.</a></p>

<%in _footer.cgi %>

<% killall -1 majestic %>
