#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="motion"
plugin_name="Motion guard"
page_title="Motion guard"
params="enabled sensitivity send2email send2ftp send2mqtt send2telegram send2webhook send2yadisk playonspeaker throttle"

[ -n "$(echo "$mj_hide_motionDetect" | sed -n "/\b${soc_family}\b/p")" ] &&
  redirect_to "/" "danger" "Motion detection is not supported on your camera."

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
    [ "false" = "$motion_send2mqtt" ] && \
    [ "false" = "$motion_send2telegram" ] && \
    [ "false" = "$motion_send2webhook" ] && \
    [ "false" = "$motion_send2yadisk" ] && \
    [ "false" = "$motion_playonspeaker" ] && \
    flash_append "danger" "You need to select at least one method of notification" && error=1
  fi

  if [ -z "$error" ]; then
    # create temp config file
    :>$tmp_file
    for _p in $params; do
      echo "${plugin}_${_p}=\"$(eval echo \$${plugin}_${_p})\"" >>$tmp_file
    done; unset _p
    mv $tmp_file $config_file

    if [ "true" = "$motion_enabled" ]; then
      if [ -z "$(eval echo "DEBUG TRACE" | sed -n "/\b$(yaml-cli -g .system.logLevel)\b/p")" ]; then
        # make required changes to majestic.yaml
        _t=$(mktemp)
        #overlayFS workaround
        #cp -f /tmp/majestic.yaml $_t
        cat /tmp/majestic.yaml > $_t
        yaml-cli -i $_t -s .system.logLevel DEBUG
        yaml-cli -i $_t -s .motionDetect.visualize true
        yaml-cli -i $_t -s .motionDetect.debug true
        mv -f $_t /tmp/majestic.yaml
        unset _t
      fi
      # touch /tmp/motionguard-restart.txt
      /etc/init.d/S92motion restart >/dev/null
    else
      /etc/init.d/S92motion stop >/dev/null
    fi

    update_caminfo
    redirect_to "$SCRIPT_NAME"
  fi
else
  include $config_file

  # Default values
  [ -z "$motion_sensitivity" ] && motion_sensitivity=45
  [ -z "$motion_throttle"    ] && motion_throttle=10
fi
%>
<%in p/header.cgi %>

<div class="row g-4 mb-4">
  <div class="col col-lg-4">
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_switch "motion_enabled" "Enable motion guard" %>
      <% field_range "motion_sensitivity" "Sensitivity" "1,50,1" "1 - minimal sensitivity, 50 - maximum sensitivity" %>
      <% field_range "motion_throttle" "Delay between notifications, sec." "1,30,1" %>
      <h5>Actions</h5>
      <ul class="list-group mb-3">
        <li class="list-group-item send2email">
          <% field_checkbox "motion_send2email" "Send to email" "<a href=\"plugin-send2email.cgi\">Configure sending to email</a>" %>
        </li>
        <li class="list-group-item send2ftp">
          <% field_checkbox "motion_send2ftp" "Upload to FTP" "<a href=\"plugin-send2ftp.cgi\">Configure uploading to FTP</a>" %>
        </li>
        <li class="list-group-item send2mqtt">
          <% field_checkbox "motion_send2mqtt" "Send to MQTT" "<a href=\"plugin-send2mqtt.cgi\">Configure sending to MQTT</a>" %>
        </li>
        <li class="list-group-item send2telegram">
          <% field_checkbox "motion_send2telegram" "Send to Telegram" "<a href=\"plugin-send2telegram.cgi\">Configure sending to Telegram</a>" %>
        </li>
        <li class="list-group-item send2webhook">
          <% field_checkbox "motion_send2webhook" "Send to webhook" "<a href=\"plugin-send2webhook.cgi\">Configure sending to a webhook</a>" %>
        </li>
        <li class="list-group-item send2yadisk">
          <% field_checkbox "motion_send2yadisk" "Upload to Yandex Disk" "<a href=\"plugin-send2yadisk.cgi\">Configure sending to Yandex Disk</a>" %>
        </li>
        <li class="list-group-item playonspeaker">
          <% field_checkbox "motion_playonspeaker" "Play sound file on speaker" "<a href=\"plugin-playonspeaker.cgi\">Configure playing on speaker</a>" %>
        </li>
      </ul>
      <% button_submit %>
    </form>
  </div>
  <div class="col col-lg-8">
    <% [ -f $config_file ] && ex "cat $config_file" %>
    <% [ -f $service_file ] && ex "cat $service_file" %>
  </div>
</div>

<script>
<% [ "true" != "$email_enabled"    ] && echo "\$('#motion_send2email').disabled = true; \$('li.send2email').clasList.add('bg-warning');" %>
<% [ "true" != "$ftp_enabled"      ] && echo "\$('#motion_send2ftp').disabled = true;" %>
<% [ "true" != "$mqtt_enabled"     ] && echo "\$('#motion_send2mqtt').disabled = true;" %>
<% [ "true" != "$telegram_enabled" ] && echo "\$('#motion_send2telegram').disabled = true;" %>
<% [ "true" != "$webhook_enabled"  ] && echo "\$('#motion_send2webhook').disabled = true;" %>
<% [ "true" != "$yadisk_enabled"   ] && echo "\$('#motion_send2yadisk').disabled = true;" %>
<% [ "true" != "$speaker_enabled"  ] && echo "\$('#motion_playonspeaker').disabled = true;" %>
</script>

<%in p/footer.cgi %>
