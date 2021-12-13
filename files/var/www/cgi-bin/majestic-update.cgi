#!/usr/bin/haserl
<%in _common.cgi %>
<%in _header.cgi %>
<h2>Updating Majestic settings</h2>
<% flash_read %>
<%
show_post() {
  echo "$(printenv | grep "POST" | grep "$1")<br>"
}

temp_yaml=/tmp/majestic.yaml

if [ -z "$POST_reset" ]; then
  command="cp -f /etc/majestic.yaml $temp_yaml"
  result=$(cp -f /etc/majestic.yaml $temp_yaml 2>&1)
else
  command="cp -f /rom/etc/majestic.yaml $temp_yaml"
  result=$(cp -f /rom/etc/majestic.yaml $temp_yaml 2>&1)
fi
report_command_info "$command" "$result"

data="$(printenv|grep POST_)"
IFS=$'\n' # make newlines the only separator
for name in $data; do
  key=".$(echo $name | sed 's/^POST_//' | cut -d= -f1 | sed 's/-/./g')"
  value="$(echo $name | cut -d= -f2)"
  oldvalue=$(yaml-cli -g "$key" -i $temp_yaml)

  [ "$key" = ".track" ] && continue
  [ "$key" = ".reset" ] && continue

  if [ "$key" = ".image.rotate" ]; then
    if [ "$value" = "0°" ]; then
      value="none"
    else
      value=${value//°/}
    fi
  fi

  if [ -z "$value" ]
  then
    if [ ! -z "$oldvalue" ]
    then
      command="yaml-cli -d \"$key\" -i /tmp/majestic.yaml -o $temp_yaml"
      result=$(yaml-cli -d "${key}" -i /tmp/majestic.yaml -o $temp_yaml 2>&1)

      report_warning "$(show_post "$key") <i class=\"small\">Empty value for ${key}. Existing value is '${oldvalue}'. Deleting.</i>"
      report_command_error "$command" "$result"
    else
      # echo "."
      report_warning "$(show_post "$key") <i class=\"small\">Empty value for ${key}. Existing value is empty, too. Skipping.</i>"
    fi
  else
    if [ "$oldvalue" != "$value" ]
    then
      command="yaml-cli -s \"$key\" \"$value\" -i $temp_yaml -o $temp_yaml"
      result=$(yaml-cli -s "${key}" "${value}" -i $temp_yaml -o $temp_yaml 2>&1)
      # "Updated value for ${key}. Existing value is '${oldvalue}'. Saving."
      report_command_info "$command" "$result"
    else
      # echo "."
      report_warning "$(show_post "$key") <i class=\"small\">Same value for ${key}. Skipping.</i>"
    fi
  fi
done

settings_changed=$(diff -q $temp_yaml /etc/majestic.yaml)
if [ ! -z "${settings_changed}" ];
then
  command="cp -f $temp_yaml /etc/majestic.yaml"
  result=$(cp -f $temp_yaml /etc/majestic.yaml 2>&1)
  report_command_info "$command" "$result"

  report_info "Settings changed."
else
  report_info "Settings not changed."
fi

command="rm $temp_yaml"
result=$(rm $temp_yaml 2>&1)
report_command_info "$command" "$result"
%>

<p class="d-grid gap-2">
  <a class="btn btn-primary" href="/cgi-bin/majestic.cgi">Go to Majestic settings</a>
  <a class="btn btn-danger" href="/cgi-bin/majestic-reset.cgi">Restore original configuration</a></p>

<div class="alert alert-info">
<pre><% diff /rom/etc/majestic.yaml /etc/majestic.yaml 2>&1 %></pre>
</div>

<%in _footer.cgi %>

<% killall -1 majestic %>
