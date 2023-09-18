#!/usr/bin/haserl
<%in p/common.cgi %>
<%
target="$GET_to"
if [ -n "$(echo "email ftp openwall telegram yadisk webhook" | sed -n "/\b${target}\b/p")" ]; then
  /usr/sbin/snapshot4cron.sh -f >/dev/null
  [ "openwall" = "$target" ] && opts="-f"
  /usr/sbin/send2${target}.sh ${opts} >/dev/null
  redirect_back "success" "Sent to ${target}."
elif [ "pastebin" = "$target" ]; then
  if [ "mjlog" = "$GET_file" ]; then
    _t=$(mktemp)
    logread | grep 'user.info majestic' >$_t
    _url=$(/usr/sbin/send2${target}.sh $_t)
    rm $_t
    unset _t
    redirect_to $_url
  fi
else
  redirect_back "danger" "Unknown target ${target}!"
fi
%>
