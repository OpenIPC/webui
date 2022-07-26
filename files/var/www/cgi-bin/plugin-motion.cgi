#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="motion"
plugin_name="Motion guard"
page_title="Motion guard"
params="enabled sensitivity send2email send2ftp send2telegram send2yadisk"

service_file=/etc/init.d/S92motion

tmp_file=/tmp/${plugin}

if [ "POST" = "$REQUEST_METHOD" ]; then
  # parse values from parameters
  for _p in $params; do
    eval ${plugin}_${_p}=\$POST_${plugin}_${_p}
    sanitize "${plugin}_${_p}"
  done; unset _p

  if [ "true" = "$motion_enabled" ]; then
    if [ "false" = "$motion_send2email" ] && [ "false" = "$motion_send2ftp" ] && [ "false" = "$motion_send2telegram" ] && [ "false" = "$motion_send2yadisk" ]; then
      flash_append "danger" "You need to select at least on method of notification"
      redirect_to "$SCRIPT_NAME"
      exit
    fi

    :>$tmp_file
    echo "#!/bin/sh" >>$tmp_file
    echo "thrashold=${motion_sensitivity}"
    echo "logread -f | grep \"Motion detected in \d* regions\" | while read BEER; do" >>$tmp_file
    echo "  [ \"\$(echo \$BEER | cut -d' ' -f4)\" -lt \"\$thrashold\" ] && exit;" >>$tmp_file
    [ "true" = "$motion_send2email"    ] && echo "  send2email.sh"    >>$tmp_file
    [ "true" = "$motion_send2ftp"      ] && echo "  send2ftp.sh"      >>$tmp_file
    [ "true" = "$motion_send2telegram" ] && echo "  send2telegram.sh" >>$tmp_file
    [ "true" = "$motion_send2yadisk"   ] && echo "  send2yadisk.sh"   >>$tmp_file
    [ "true" = "$motion_send2yucca"    ] && echo "  send2yucca.sh"    >>$tmp_file
    echo "done &" >>$tmp_file
    mv $tmp_file $service_file
    chmod +x $service_file
    touch /tmp/motionguard-restart.txt
    redirect_to "$SCRIPT_NAME"
  else
    [ -f $service_file ] && rm $service_file
    redirect_to "$SCRIPT_NAME"
  fi
fi

[ -z "$motion_sensitivity" ] && motion_sensitivity=3
if [ -f "$service_file" ]; then
  motion_enabled="true"
  [ -n "$(grep send2email.sh $service_file)"    ] && motion_send2email="true"
  [ -n "$(grep send2ftp.sh $service_file)"      ] && motion_send2ftp="true"
  [ -n "$(grep send2telegram.sh $service_file)" ] && motion_send2telegram="true"
  [ -n "$(grep send2yadisk.sh $service_file)"   ] && motion_send2yadisk="true"
  [ -n "$(grep send2yucca.sh $service_file)"    ] && motion_send2yucca="true"
fi
%>
<%in p/header.cgi %>

<form action="<%= $SCRIPT_NAME %>" method="post">
  <% field_switch "motion_enabled" "Enable motion guard" %>
  <div class="row g-4 mb-4">
    <div class="col col-lg-4">
      <% field_range "motion_sensitivity" "Sensitivity" "1,5,1" "1 - minimal sensitivity, 5 - maximum sensitivity" %>
      <% field_checkbox "motion_send2email" "Send to email" "<a href=\"plugin-send2email.cgi\">Configure sending to email</a>" %>
      <% field_checkbox "motion_send2ftp" "Upload to FTP" "<a href=\"plugin-send2ftp.cgi\">Configure uploading to FTP</a>" %>
      <% field_checkbox "motion_send2telegram" "Send to Telegram" "<a href=\"plugin-send2telegram.cgi\">Configure sending to Telegram</a>" %>
      <% field_checkbox "motion_send2yadisk" "Upload to Yandex Disk" "<a href=\"plugin-send2yadisk.cgi\">Configure sending to Yandex Disk</a>" %>
      <% field_checkbox "motion_send2yucca" "Notify Yucca NVR" "<a href=\"plugin-send2yucca.cgi\">Configure notification of Yucca NVR</a>" %>
      <% button_submit %>
    </div>
    <div class="col col-lg-8">
      <% [ -f $service_file ] && ex "cat $service_file" %>
    </div>
  </div>
</form>

<script>
<% [ "true" != "$email_enabled"    ] && echo "\$('#motion_send2email').disabled = true;" %>
<% [ "true" != "$ftp_enabled"      ] && echo "\$('#motion_send2ftp').disabled = true;" %>
<% [ "true" != "$telegram_enabled" ] && echo "\$('#motion_send2telegram').disabled = true;" %>
<% [ "true" != "$yadisk_enabled"   ] && echo "\$('#motion_send2yadisk').disabled = true;" %>
<% [ "true" != "$yucca_enabled"    ] && echo "\$('#motion_send2yucca').disabled = true;" %>
</script>

<%in p/footer.cgi %>
