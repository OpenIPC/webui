#!/usr/bin/haserl
content-type: text/html

<%
action=$FORM_action
sense=$FORM_sense
%>
<%in _header.cgi %>

<%
case $action in
  Save)
    echo "<h1>Trying to update...</h1>"
    for name in "$(printenv | grep "FORM_\.")"; do
      key=$(echo $name | cut -d= -f1 | cut -d_ -f2)
      value=$(echo $name | cut -d= -f2)

      echo "Probe change ${key} to ${value} at majestic.yaml" | logger -t microbe-web

      [   ${value} ] && yaml-cli -s $key $value
      [ ! ${value} ] && yaml-cli -d $key
    done
    killall -1 majestic

    echo "<script>setTimeout('window.location=\"/cgi-bin/majestic.cgi\"', 3000);</script>"
    ;;
esac
%>
<%in _footer.cgi %>
