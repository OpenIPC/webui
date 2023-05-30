#!/usr/bin/haserl
<%in p/common.cgi %>
<%
[ -z "$GET_f" ] && append_flash "danger" "Nothing to restore." && error=1

file=$GET_f
[ ! -f "/rom/${file}" ] && append_flash "danger" "File /rom/${file} not found!" && error=1

[ -n "$error" ] && redirect_back

cp "/rom/${file}" "${file}"
if [ $? -eq 0 ]; then
  redirect_back "success" "File ${file} restored to firmware defaults."
else
  redirect_back "danger" "Cannot restore ${file}!"
fi
%>
