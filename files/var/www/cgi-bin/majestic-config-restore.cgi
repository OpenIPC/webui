#!/usr/bin/haserl --upload-limit=1024 --upload-dir=/tmp
<%in _common.cgi %>
<%
config_file=/etc/majestic.yaml
magicnum="23206d616a6573746963"
error=""
if [ -z "$POST_upfile_name"  ]; then
  error="No file found! Did you forget to upload?"
elif [ ! -r "$POST_upfile" ]; then
  error="Cannot read file \"${POST_upfile_name}\" from \"${POST_upfile}\"!"
elif [ "$(wc -c "$POST_upfile" | awk '{print $1}')" -gt "$maxsize" ]; then
  error="File \"${POST_upfile_name}\" is too large! Its size is $(wc -c "$POST_upfile" | awk '{print $1}') bytes, but it should be ${maxsize} bytes or less."
#elif [ "$magicnum" -ne "$(xxd -p -l 10 "$POST_upfile")" ]; then
#  error="File magic number does not match. Did you upload a wrong file? $(xxd -p -l 10 "$POST_upfile") != $magicnum"
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
