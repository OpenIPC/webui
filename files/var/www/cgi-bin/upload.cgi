#!/usr/bin/haserl --upload-limit=4096 --upload-dir=/tmp
content-type: text/html

<%in _header.cgi %>
<h2>Uploading file</h2>
<%
case $FORM_action in
  kernel)
    maxsize=1500
    target="/etc/openvpn/ca.crt"
    ;;
  rootfs)
    maxsize=5000
    target="/etc/openvpn/cert.crt"
    ;;
esac

if [ -z "$FORM_upfile_name" ]
then
  echo "<div class=\"alert alert-danger\">" \
    "<b>Error: no file found!</b><br>Did you forget to upload?" \
    "</div>"
else
  if [ ! -r "$FORM_upfile" ]
  then
    echo "<div class=\"alert alert-danger\">" \
      "<b>Error: cannot read file \"${FORM_upfile_name}\" from \"${FORM_upfile}\"!</b>" \
      "</div>"
  else
    fsize="$(wc -c "$FORM_upfile" | awk '{print $1}')"
    if [ $fsize -gt $maxsize ]
    then
      echo "<div class=\"alert alert-danger\">" \
        "<b>Error: file \"${FORM_upfile_name}\" is so big!</b><br>" \
        "Its size is ${fsize} bytes, while it should be ${maxsize} bytes or less." \
        "</div>"
    else
      echo "<pre># cp \"$FORM_upfile\" \"$target\" 2>&1</pre>"
      if cp "$FORM_upfile" "$target" 2>&1
      then
        rm "$FORM_upfile"
        echo "<h3>Trying to upload...</h3>"
      else
        echo "<div class=\"alert alert-danger\">" \
          "<b>Error: unable to write file \"${FORM_upfile_name}\" to flash!</b>" \
          "</div>"
      fi
    fi
  fi
fi
%>
<p><a href="/cgi-bin/index.cgi">Go back to settings</a></p>
<%in _footer.cgi %>
