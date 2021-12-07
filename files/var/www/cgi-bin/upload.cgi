#!/usr/bin/haserl --upload-limit=6810 --upload-dir=/tmp
content-type: text/html

<%in _header.cgi %>
<h2>Uploading <%= $FORM_action %> file</h2>
<%
case $FORM_action in
  kernel)
    maxsize=2097152
    target="/etc/openvpn/ca.crt"
    magicnum="27051956"
    ;;
  rootfs)
    maxsize=5242880
    target="/etc/openvpn/cert.crt"
    magicnum="68737173"
    ;;
esac

err=""
if [ -z "$FORM_upfile_name"  ]; then
  err="no file found! Did you forget to upload?"
elif [ ! -r "$FORM_upfile" ]; then
  err="cannot read file \"${FORM_upfile_name}\" from \"${FORM_upfile}\"!"
elif [ "$(wc -c "$FORM_upfile" | awk '{print $1}')" -gt "$maxsize" ]; then
  err="file \"${FORM_upfile_name}\" is too large! Its size is $(wc -c "$FORM_upfile" | awk '{print $1}') bytes, but it should be ${maxsize} bytes or less."
elif [ "$magicnum" -ne "$(xxd -p -l 4 "$FORM_upfile")" ]; then
  err="File magic number does not match. Did you upload a wrong file? $(xxd -p -l 4 "$FORM_upfile") != $magicnum"
fi

if [ -z "$err" ]; then
  echo "<pre># cp \"$FORM_upfile\" \"$target\" 2>&1</pre>"
  if cp "$FORM_upfile" "$target" 2>&1
  then
    rm "$FORM_upfile"
    echo "<h3>Trying to upload...</h3>"
  else
    echo "<div class=\"alert alert-danger\"><b>Error: unable to write file \"${FORM_upfile_name}\" to flash!</b></div>"
  fi
else
  echo "<div class=\"alert alert-danger\"><b>Error: ${err}</b></div>"
fi
%>
<p><a href="/cgi-bin/updates.cgi">Go back to firmware updates page</a></p>
<%in _footer.cgi %>
