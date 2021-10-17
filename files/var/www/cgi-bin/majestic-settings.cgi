#!/usr/bin/haserl
<?
  export PATH=/bin:/sbin:/usr/bin:/usr/sbin
  action=$FORM_action
  sense=$FORM_sense
  #
  echo "Content-type: text/html"
  echo
  echo "<html><body><div align=center>"
  echo "<img src=\"https://openipc.org/images/logo_openipc.png\" width=\"256\">"
  echo

  echo
  case $action in
    Save)
      echo "<br><br><br><br><br><center><h1>We try to update...</h1></center>"
      for name in $(printenv | grep "FORM_\."); do
        key=$(echo $name | cut -d= -f1 | cut -d_ -f2)
        value=$(echo $name | cut -d= -f2)
        
        echo "Probe change ${key} to ${value} at majestic.yaml" | logger -t microbe-web
        
        [   ${value} ] && yaml-cli -s $key $value
        [ ! ${value} ] && yaml-cli -d $key $value
      done
      killall -1 majestic
      echo "<script language=javascript>setTimeout('window.location=\"/cgi-bin/majestic.cgi\"',1000);</script>"
      ;;
  esac
  echo
  echo "</div></body></html>"
?>
