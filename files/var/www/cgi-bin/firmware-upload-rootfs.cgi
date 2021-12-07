#!/usr/bin/haserl --upload-limit=5120 --upload-dir=/tmp
<%
maxsize=5242880
magicnum="68737173"

sysupgrade_date=$(ls -lc --full-time /usr/sbin/sysupgrade | xargs | cut -d " " -f 6)
sysupgrade_date=$(date --date="$sysupgrade_date" +"%s")
new_sysupgrade_date=$(date --date="2021-12-07" +"%s")

error=""
if [ -z "$FORM_upfile_name"  ]; then
  error="no file found! Did you forget to upload?"
elif [ ! -r "$FORM_upfile" ]; then
  error="cannot read file \"${FORM_upfile_name}\" from \"${FORM_upfile}\"!"
elif [ "$(wc -c "$FORM_upfile" | awk '{print $1}')" -gt "$maxsize" ]; then
  error="file \"${FORM_upfile_name}\" is too large! Its size is $(wc -c "$FORM_upfile" | awk '{print $1}') bytes, but it should be ${maxsize} bytes or less."
elif [ "$magicnum" -ne "$(xxd -p -l 4 "$FORM_upfile")" ]; then
  error="File magic number does not match. Did you upload a wrong file? $(xxd -p -l 4 "$FORM_upfile") != $magicnum"
elif [ "$sysupgrade_date" -ge "$new_sysupgrade_date" ]; then
  error="This feature requires the latest sysupgrade tool. Please upgrade firmware first."
fi

if [ ! -z "$error" ]; then %>
<%in _header.cgi %>
<h2 class="text-danger">Oops. Something happened.</h2>
<div class="alert alert-danger"><%= $error %></div>
<%in _footer.cgi %>
<% else
  echo "HTTP/1.1 302 Moved Temporarily"
  echo "Content-type: text/html; charset=UTF-8"
  echo "Date: $(TZ=GMT date +"%a, %d %b %Y %T %Z")"
  echo "Location: /cgi-bin/progress.cgi"
  echo "Server: httpd"
  echo "Status: 302 Moved Temporarily"

  mv ${FORM_upfile} /tmp/${FORM_upfile_name}
  sysupgrade --rootfs=/tmp/${FORM_upfile_name}
fi
%>
