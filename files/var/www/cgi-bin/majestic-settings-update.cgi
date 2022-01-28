#!/usr/bin/haserl
<%in _common.cgi %>
<%
mj_conf=/etc/majestic.yaml
orig_yaml=/tmp/majestic.yaml.original
temp_yaml=/tmp/majestic.yaml

if [ ! -z "$DEBUG" ]; then %>
<%in _debug.cgi %>
<%
  cp -f ${mj_conf} ${orig_yaml}
fi

cp -f ${mj_conf} ${temp_yaml}
debug_message "cp -f ${mj_conf} ${temp_yaml}"

data="$(printenv|grep POST_)"
IFS=$'\n' # make newlines the only separator
for name in $data; do
  key=".$(echo $name | sed 's/^POST_//' | cut -d= -f1 | sed 's/-/./g')"
  value="$(echo $name | cut -d= -f2)"

  # validation and normalization
  [ "$key" = ".go.to" ] && goto=${value} && continue
  [ "$key" = ".track" ] && continue
  [ "$key" = ".reset" ] && continue
  [ "$key" = ".netip.password.plain" ] && continue
  if [ "$key" = ".image.rotate" ]; then
    if [ "$value" = "0°" ]; then
      value="none"
    else
      value=${value//°/}
    fi
  fi

  oldvalue=$(yaml-cli -g "$key" -i ${temp_yaml})
  if [ -z "$value" ]; then
    if [ ! -z "$oldvalue" ]; then
      yaml-cli -d $key -i ${temp_yaml} -o ${temp_yaml}
      debug_message "yaml-cli -d $key -i ${temp_yaml} -o ${temp_yaml}"
    fi
  else
    if [ "$oldvalue" != "$value" ]; then
      yaml-cli -s $key "$value" -i ${temp_yaml} -o ${temp_yaml}
      debug_message "yaml-cli -s $key "$value" -i ${temp_yaml} -o ${temp_yaml}"
    fi
  fi
done

if [ ! -z $(diff -q ${temp_yaml} ${mj_conf}) ]; then
  cp -f ${temp_yaml} ${mj_conf}
  debug_message "cp -f ${temp_yaml} ${mj_conf}"
fi

rm ${temp_yaml}
debug_message "rm ${temp_yaml}"

if [ -z "$DEBUG" ]; then
  killall -1 majestic
  if [ -n "$goto" ]; then
    redirect_to ${goto}
  else
    redirect_to "/cgi-bin/majestic-config-compare.cgi"
  fi
else
  debug_message "diff ${orig_yaml} ${mj_conf}"
  diff ${orig_yaml} ${mj_conf}
#  rm ${orig_yaml}
  debug_message "done."
fi
%>
