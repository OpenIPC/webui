#!/usr/bin/haserl
<%in _common.cgi %>
<%
temp_yaml=/tmp/majestic.yaml

if [ ! -z "$DEBUG" ]; then %>
<%in _debug.cgi %>
<%
  cp -f /etc/majestic.yaml /tmp/majestic.yaml.original
fi

cp -f /etc/majestic.yaml $temp_yaml
debug_message "cp -f /etc/majestic.yaml $temp_yaml"

data="$(printenv|grep POST_)"
IFS=$'\n' # make newlines the only separator
for name in $data; do
  key=".$(echo $name | sed 's/^POST_//' | cut -d= -f1 | sed 's/-/./g')"
  value="$(echo $name | cut -d= -f2)"

  # validation and normalization
  [ "$key" = ".track" ] && continue
  [ "$key" = ".reset" ] && continue
  if [ "$key" = ".image.rotate" ]; then
    if [ "$value" = "0°" ]; then
      value="none"
    else
      value=${value//°/}
    fi
  fi

  oldvalue=$(yaml-cli -g "$key" -i $temp_yaml)
  if [ -z "$value" ]; then
    if [ ! -z "$oldvalue" ]; then
      yaml-cli -d $key -i $temp_yaml -o $temp_yaml
      debug_message "yaml-cli -d $key -i $temp_yaml -o $temp_yaml"
    fi
  else
    if [ "$oldvalue" != "$value" ]; then
      yaml-cli -s $key "$value" -i $temp_yaml -o $temp_yaml
      debug_message "yaml-cli -s $key "$value" -i $temp_yaml -o $temp_yaml"
    fi
  fi
done

if [ ! -z $(diff -q $temp_yaml /etc/majestic.yaml) ]; then
  cp -f $temp_yaml /etc/majestic.yaml
  debug_message "cp -f $temp_yaml /etc/majestic.yaml"
fi

rm $temp_yaml
debug_message "rm $temp_yaml"

if [ -z "$DEBUG" ]; then
  # killall -1 majestic
  /etc/init.d/S95hisilicon restart
  redirect_to "/cgi-bin/majestic-config-compare.cgi"
else
  debug_message "diff /tmp/majestic.yaml.original /etc/majestic.yaml"
  diff /tmp/majestic.yaml.original /etc/majestic.yaml
#  rm /tmp/majestic.yaml.original
  debug_message "done."
fi
%>
