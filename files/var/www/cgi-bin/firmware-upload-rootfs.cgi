#!/usr/bin/haserl --upload-limit=5120 --upload-dir=/tmp
<%in _common.cgi %>
<%
maxsize=5242880
magicnum="68737173"

sysupgrade_date=$(ls -lc --full-time /usr/sbin/sysupgrade | xargs | cut -d " " -f 6)
sysupgrade_date=$(date --date="$sysupgrade_date" +"%s")
new_sysupgrade_date=$(date --date="2021-12-07" +"%s")

error=""
if [ -z "$POST_upfile_name"  ]; then
  error="No file found! Did you forget to upload?"
elif [ ! -r "$POST_upfile" ]; then
  error="Cannot read file \"${POST_upfile_name}\" from \"${POST_upfile}\"!"
elif [ "$(wc -c "$POST_upfile" | awk '{print $1}')" -gt "$maxsize" ]; then
  error="File \"${POST_upfile_name}\" is too large! Its size is $(wc -c "$POST_upfile" | awk '{print $1}') bytes, but it should be ${maxsize} bytes or less."
elif [ "$magicnum" -ne "$(xxd -p -l 4 "$POST_upfile")" ]; then
  error="File magic number does not match. Did you upload a wrong file? $(xxd -p -l 4 "$POST_upfile") != $magicnum"
elif [ "$sysupgrade_date" -lt "$new_sysupgrade_date" ]; then
  error="This feature requires the latest sysupgrade tool. Please upgrade firmware first."
fi

if [ ! -z "$error" ]; then %>
<%in _header.cgi %>
<% report_error "$error" %>
<%in _footer.cgi %>
<% else
  redirect_to "/cgi-bin/progress.cgi"

  mv ${POST_upfile} /tmp/${POST_upfile_name}
  sysupgrade -f --rootfs=/tmp/${POST_upfile_name}
fi
%>
