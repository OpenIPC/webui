#!/usr/bin/haserl
<%in _common.cgi %>
<%in _header.cgi %>
<h2>Updating Majestic settings</h2>
<%
cp -f /etc/majestic.yaml /tmp/majestic.yaml
data="$(printenv|grep POST_)"
IFS=$'\n' # make newlines the only separator
for name in $data; do
  key=".$(echo $name | sed 's/^POST_//' | cut -d= -f1 | sed 's/-/./g')"
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
    if [ ! -z "$oldvalue" ]
    then
      command="yaml-cli -d \"$key\" -i /tmp/majestic.yaml -o /tmp/majestic.yaml"
      result=$(yaml-cli -d \"$key\" -i /tmp/majestic.yaml -o /tmp/majestic.yaml 2>&1)
#     report_warning "Empty value for ${key}. Existing value is '${oldvalue}'. Deleting."
      report_command_error "$command" "$result"
    else
      echo "."
#     report_warning "Empty value for ${key}. Existing value is empty, too. Skipping."
    fi
  else
    if [ "$oldvalue" != "$value" ]
    then
      command="yaml-cli -s \"$key\" \"$value\" -i /tmp/majestic.yaml -o /tmp/majestic.yaml"
      result=$(yaml-cli -s \"$key\" \"$value\" -i /tmp/majestic.yaml -o /tmp/majestic.yaml 2>&1)
      # "Updated value for ${key}. Existing value is '${oldvalue}'. Saving."
      report_command_info "$command" "$result"
    else
      echo "."
#     report_warning "Same value for ${key}. Skipping."
    fi
  fi
done

settings_changed=$(diff -q /tmp/majestic.yaml /etc/majestic.yaml)
if [ ! -z "${settings_changed}" ];
then
  report_info "Settings changed."
  cp -f /tmp/majestic.yaml /etc/majestic.yaml
else
  report_info "Settings not changed."
fi
rm /tmp/majestic.yaml
%>

<p class="d-grid gap-2">
  <a class="btn btn-primary" href="/cgi-bin/majestic.cgi">Go to Majestic settings</a>
  <a class="btn btn-danger" href="/cgi-bin/majestic-reset.cgi">Restore original configuration</a></p>

<%in _footer.cgi %>

<% killall -1 majestic %>
