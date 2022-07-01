#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="tz"
page_title="Timezone"

config_file="${ui_config_dir}/${plugin}.conf"
[ ! -f "$config_file" ] && touch $config_file

if [ "POST" = "$REQUEST_METHOD" ]; then
  tmp_file=/tmp/${plugin}.conf
  :> $tmp_file
  [ -z "$POST_tz_name" ] && redirect_to $SCRIPT_NAME "warning" "Empty timezone name. Skipping."
  [ -z "$POST_tz_data" ] && redirect_to $SCRIPT_NAME "warning" "Empty timezone value. Skipping."
  [ "$tz_data" != "$POST_tz_data" ] && echo "${POST_tz_data}" > /etc/TZ
  [ "$tz_name" != "$POST_tz_name" ] && echo "${POST_tz_name}" > /etc/tz_name
  update_caminfo
  redirect_to $SCRIPT_NAME "success" "Timezone updated."
fi
%>

<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-xxl-3 g-4">
  <div class="col">
    <h3>Set up timezone</h3>
    <p><a href="#" id="frombrowser">Pick up from browser</a></p>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <datalist id="tz_list"></datalist>
      <p class="string">
        <label for="tz_name" class="form-label">Zone name</label>
        <input type="text" id="tz_name" name="tz_name" value="<%= $tz_name %>" class="form-control" list="tz_list">
        <span class="hint text-secondary">Start typing the name of the nearest large city in the box above then select from available variants.</span>
      </p>
      <p class="string">
        <label for="tz_data" class="form-label">Zone string</label>
        <input type="text" id="tz_data" name="tz_data" value="<%= $tz_data %>" class="form-control" readonly>
        <span class="hint text-secondary">Control string of the timezone selected above. Read-only field, only for monitoring.</span>
      </p>
      <% button_submit %>
    </form>
  </div>
  <div class="col">
    <h3>Config files</h3>
    <% ex "cat /etc/tz_name" %>
    <% ex "cat /etc/TZ" %>
  </div>
  <div class="col">
    <h3>System settings</h3>
    <% ex "echo \$TZ" %>
  </div>
</div>

<script src="/a/tz.js"></script>
<%in p/footer.cgi %>
