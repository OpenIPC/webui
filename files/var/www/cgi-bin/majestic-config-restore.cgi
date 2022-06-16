#!/usr/bin/haserl --upload-limit=1024 --upload-dir=/tmp
<%in _common.cgi %>
<%
config_file=/etc/majestic.yaml
magicnum="23206d616a6573746963"

file=$POST_mj_restore_file
file_name=$POST_mj_restore_file_name

error=""
if [ -z "$file_name" ]; then
  error="$tMsgNoUploadedFileFound"
elif [ ! -r "$file" ]; then
  error="$tMsgCannotReadUploadedFile"
elif [ "$(wc -c "$file" | awk '{print $1}')" -gt "$maxsize" ]; then
  error="$tMsgUploadedFileIsTooLarge $(wc -c $file | awk '{print $1}') > ${maxsize}."
#elif [ "$magicnum" -ne "$(xxd -p -l 10 $file)" ]; then
#  error="$tMsgUploadedFileHasWrongMagic $(xxd -p -l 10 $file) != $magicnum"
fi

if [ -n "$error" ]; then %>
<%in _header.cgi %>
<% report_error "$error" %>
<%in _footer.cgi %>
<% else
# yaml-cli -i $POST_upfile -o /tmp/majestic.yaml # FIXME: sanitize
mv $file_path /etc/majestic.yaml
redirect_to "/cgi-bin/majestic-config-compare.cgi"
fi
%>
