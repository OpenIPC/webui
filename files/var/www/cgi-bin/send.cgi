#!/usr/bin/haserl
<%in p/common.cgi %>
<%
target="$GET_to"
if [ -n "$(echo "email ftp openwall telegram yadisk" | sed -n "/\b${target}\b/p")" ]; then
  /usr/sbin/send2${target}.sh >/dev/null
  redirect_back "success" "Sent to ${target}."
else
  redirect_back "danger" "Unknown target ${target}!"
fi
%>
