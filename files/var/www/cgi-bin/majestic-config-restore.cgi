#!/usr/bin/haserl --upload-limit=1024 --upload-dir=/tmp
<%in _common.cgi %>
<%
config_file=/etc/majestic.yaml
magicnum="23206d616a6573746963"
error=""
if [ -z "$POST_upfile_name"  ]; then
  error="$tMsgNoUploadedFileFound"
elif [ ! -r "$POST_upfile" ]; then
  error="$tMsgCannotReadUploadedFile"
elif [ "$(wc -c "$POST_upfile" | awk '{print $1}')" -gt "$maxsize" ]; then
  error="$tMsgUploadedFileIsTooLarge $(wc -c "$POST_upfile" | awk '{print $1}') > ${maxsize}."
#elif [ "$magicnum" -ne "$(xxd -p -l 10 "$POST_upfile")" ]; then
#  error="$tMsgUploadedFileHasWrongMagic $(xxd -p -l 10 "$POST_upfile") != $magicnum"
fi
if [ ! -z "$error" ]; then %>
<%in _header.cgi %>
<% report_error "$error" %>
<%in _footer.cgi %>
<% else
# yaml-cli -i ${POST_upfile} -o /tmp/majestic.yaml # FIXME: sanitize
mv /tmp/majestic.yaml /etc/majestic.yaml
redirect_to "/cgi-bin/majestic-config-compare.cgi"
fi
%>
