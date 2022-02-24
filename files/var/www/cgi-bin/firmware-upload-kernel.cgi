#!/usr/bin/haserl --upload-limit=2048 --upload-dir=/tmp
<%in _common.cgi %>
<%in _header.cgi %>
<%
maxsize=2097152
magicnum="27051956"

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

if [ ! -z "$error" ]; then
  report_error "$error"
else
%>
<pre class="bg-light p-4 log-scroll">
<%
  mv ${POST_upfile} /tmp/${POST_upfile_name}
  sysupgrade --kernel=/tmp/${POST_upfile_name} --force_ver
%>
</pre>
<a class="btn btn-primary" href="/"><%= $tButtonGoHome %></a>
<% fi %>
<%in _footer.cgi %>
