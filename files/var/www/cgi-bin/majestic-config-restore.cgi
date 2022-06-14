#!/usr/bin/haserl --upload-limit=1024 --upload-dir=/tmp
<%in _common.cgi %>
<%
config_file=/etc/majestic.yaml
magicnum="23206d616a6573746963"
error=""
if [ -z "$POST_mj_restore_file_name"  ]; then
  error="$tMsgNoUploadedFileFound"
elif [ ! -r "$POST_mj_restore_file" ]; then
  error="$tMsgCannotReadUploadedFile"
elif [ "$(wc -c "$POST_mj_restore_file" | awk '{print $1}')" -gt "$maxsize" ]; then
  error="$tMsgUploadedFileIsTooLarge $(wc -c "$POST_mj_restore_file" | awk '{print $1}') > ${maxsize}."
#elif [ "$magicnum" -ne "$(xxd -p -l 10 "$POST_mj_restore_file")" ]; then
#  error="$tMsgUploadedFileHasWrongMagic $(xxd -p -l 10 "$POST_mj_restore_file") != $magicnum"
fi

if [ ! -z "$error" ]; then %>
<%in _header.cgi %>
<% report_error "$error" %>
<%in _footer.cgi %>
<% else
# yaml-cli -i ${POST_upfile} -o /tmp/majestic.yaml # FIXME: sanitize
mv "$POST_mj_restore_file_path" /etc/majestic.yaml
redirect_to "/cgi-bin/majestic-config-compare.cgi"
fi
%>
