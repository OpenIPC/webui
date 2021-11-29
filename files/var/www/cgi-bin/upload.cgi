#!/usr/bin/haserl --upload-limit=4096 --upload-dir=/tmp/
content-type: text/html

<%
action=$FORM_action
upfile=$FORM_upfile
%>
<%in _header.cgi %>
<%
echo "Probe write ${action} file" | logger -t microbe-web

case $action in
  kernel)
    if [ -r $upfile ]; then
      fsize="$(wc -c $upfile | awk '{print $1}')"
      if [ $fsize -gt "1500" ]; then
        echo "<h1 class=\"red\">Error: file is so big!</h1>"
      else
        if cp $upfile /etc/openvpn/ca.crt 2>/dev/null; then
          ok=1
          rm $upfile
        else
          echo "<h1 class=\"red\">Error: unable to write file to flash!</h1>"
        fi
      fi
    else
      echo "<h1 class=\"red\">Error: file not found!</h1>"
    fi
    [ $ok ] && echo "<h1>Trying to upload...</h1>"
  ;;
  rootfs)
    if [ -r $upfile ]; then
      fsize="$(wc -c $upfile | awk '{print $1}')"
      if [ $fsize -gt "5000" ]; then
        echo "<h1 class=\"red\">Error: file is so big!</h1>"
      else
        if cp $upfile /etc/openvpn/cert.crt 2>/dev/null; then
          ok=1
          rm $upfile
        else
          echo "<h1 class=\"red\">Error: unable to write file to flash!</h1>"
        fi
      fi
    else
      echo "<h1 class=\"red\">Error: file not found!</h1>"
    fi
    [ $ok ] && echo "<h1>Trying to upload...</h1>"
  ;;
esac
%>
<script>setTimeout('window.location="/cgi-bin/index.cgi"', 3000);</script>
<%in _footer.cgi %>
