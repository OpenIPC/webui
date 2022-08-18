#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="motion"
plugin_name="Motion guard"
page_title="Motion guard"
params="enabled sensitivity send2email send2ftp send2telegram send2yadisk"

[ -n "$(echo "$mj_hide_motionDetect" | sed -n "/\b${soc_family}\b/p")" ] && redirect_to "/" "danger" "Motion detection is not supported on your camera."

service_file=/etc/init.d/S92motion
tmp_file=/tmp/${plugin}

config_file="${ui_config_dir}/${plugin}.conf"
[ ! -f "$config_file" ] && touch $config_file

if [ "POST" = "$REQUEST_METHOD" ]; then
  # parse values from parameters
  for _p in $params; do
    eval ${plugin}_${_p}=\$POST_${plugin}_${_p}
    sanitize "${plugin}_${_p}"
  done; unset _p

  ### Validation
  if [ "true" = "$motion_enabled" ]; then
    [ "false" = "$motion_send2email" ] && \
    [ "false" = "$motion_send2ftp" ] && \
    [ "false" = "$motion_send2telegram" ] && \
    [ "false" = "$motion_send2yadisk" ] && \
    flash_append "danger" "You need to select at least one method of notification" && error=1
  fi

  if [ -z "$error" ]; then
    # create temp config file
    :>$tmp_file
    for _p in $params; do
      echo "${plugin}_${_p}=\"$(eval echo \$${plugin}_${_p})\"" >>$tmp_file
    done; unset _p
    mv $tmp_file $config_file

    update_caminfo

    # create service file
    if [ "true" = "$motion_enabled" ]; then
      :>$tmp_file
      echo "#!/bin/sh" >>$tmp_file
      echo "threshold=${motion_sensitivity}" >>$tmp_file
      echo "logread -f | grep \"Motion detected in \d* regions\" | while read BEER; do" >>$tmp_file
      echo "  [ \"\$(echo \$BEER | cut -d' ' -f4)\" -lt \"\$threshold\" ] && exit;" >>$tmp_file
      echo "  snapshot4cron.sh -f" >>$tmp_file
      echo "  [ $? -ne 0 ] && echo \"Cannot get a snapshot\" && exit 2" >>$tmp_file
      [ "true" = "$motion_send2email"    ] && echo "  send2email.sh"    >>$tmp_file
      [ "true" = "$motion_send2ftp"      ] && echo "  send2ftp.sh"      >>$tmp_file
      [ "true" = "$motion_send2telegram" ] && echo "  send2telegram.sh" >>$tmp_file
      [ "true" = "$motion_send2yadisk"   ] && echo "  send2yadisk.sh"   >>$tmp_file
      echo "done &" >>$tmp_file
      mv $tmp_file $service_file
      chmod +x $service_file
      touch /tmp/motionguard-restart.txt
      redirect_to "$SCRIPT_NAME"
    fi

    # remove service file
    if [ "false" = "$motion_enabled" ]; then
      [ -f $service_file ] && rm $service_file
      touch /tmp/motionguard-restart.txt
      redirect_to "$SCRIPT_NAME"
    fi
  fi
else
  include $config_file

  # Default values
  [ -z "$motion_sensitivity" ] && motion_sensitivity=3
  if [ -f "$service_file" ]; then
    motion_enabled="true"
    [ -n "$(grep send2email.sh $service_file)"    ] && motion_send2email="true"
    [ -n "$(grep send2ftp.sh $service_file)"      ] && motion_send2ftp="true"
    [ -n "$(grep send2telegram.sh $service_file)" ] && motion_send2telegram="true"
    [ -n "$(grep send2yadisk.sh $service_file)"   ] && motion_send2yadisk="true"
  fi
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
      <% button_submit %>
    </div>
    <div class="col col-lg-8">
      <% [ -f $config_file ] && ex "cat $config_file" %>
      <% [ -f $service_file ] && ex "cat $service_file" %>
    </div>
  </div>
</form>

<script>
<% [ "true" != "$email_enabled"    ] && echo "\$('#motion_send2email').disabled = true;" %>
<% [ "true" != "$ftp_enabled"      ] && echo "\$('#motion_send2ftp').disabled = true;" %>
<% [ "true" != "$telegram_enabled" ] && echo "\$('#motion_send2telegram').disabled = true;" %>
<% [ "true" != "$yadisk_enabled"   ] && echo "\$('#motion_send2yadisk').disabled = true;" %>
</script>

<%in p/footer.cgi %>
