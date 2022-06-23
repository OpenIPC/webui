#!/usr/bin/haserl --upload-limit=20 --upload-dir=/tmp
<%in p/common.cgi %>
<%
config_file=/etc/majestic.yaml
magicnum="23206d616a6573746963"

file="$POST_mj_restore_file"
file_name="$POST_mj_restore_file_name"
file_path="$POST_mj_restore_file_path"

error=""
if [ -z "$file_name" ]; then
  error="$t_form_error_1"
elif [ ! -r "$file" ]; then
  error="$t_form_error_2"
elif [ "$(wc -c "$file" | awk '{print $1}')" -gt "$maxsize" ]; then
  error="$t_form_error_3 $(wc -c $file | awk '{print $1}') > ${maxsize}."
#elif [ "$magicnum" -ne "$(xxd -p -l 10 $file)" ]; then
#  error="$t_form_error_4 $(xxd -p -l 10 $file) != $magicnum"
fi

if [ -n "$error" ]; then %>
<%in p/header.cgi %>
<% report_error "$error" %>
<%in p/footer.cgi %>
<% else
# yaml-cli -i $POST_upfile -o /tmp/majestic.yaml # FIXME: sanitize
mv $file_path /etc/majestic.yaml
redirect_to "/cgi-bin/majestic-config-compare.cgi"
fi
%>
