#!/usr/bin/haserl
<%
get_system_info

button() {
  id=$(echo "${2// /-}" | tr '[:upper:]' '[:lower:]' | tr -cd '[:alnum:]-' )
  echo "<img id=\"${id}\" src=\"/img/${1}\" alt=\"${2}\" title=\"${2}\">"
}
%>
<div class="alert alert-danger"><%= $tMsgPtzNotWorking %></div>
<div class="control-board row">
<div class="control col-lg-4">
<% button "arrow-ul.svg" "Pan up left" %>
<% button "arrow-uc.svg" "Pan up" %>
<% button "arrow-ur.svg" "Pan up right" %>
<% button "arrow-cl.svg" "Pan left" %>
<% button "arrow-cr.svg" "Pan right" %>
<% button "arrow-dl.svg" "Pan down left" %>
<% button "arrow-dc.svg" "Pan down" %>
<% button "arrow-dr.svg" "Pan down right" %>
<% button "speed-slow.svg" "Speed" %>
<% button "zoom-close.svg" "Zoom in" %>
<% button "zoom-far.svg" "Zoom out" %>
<% button "focus-plus.svg" "Focus: plus" %>
<% button "focus-auto.svg" "Focus: auto" %>
<% button "focus-minus.svg" "Focus: minus" %>
<% [ "true" = "$(yaml-cli -g .nightMode.enabled)" ] && button "light-off.svg" "Night mode" %>
<% [ -f /etc/telegram.cfg ] && [ $(cat /etc/telegram.cfg | wc -l) -ge 2 ] && button "telegram.svg" "Send to Telegram" %>
</div>

<div class="control col-6 col-lg-2">
<% button "image-rotate-cw.svg" "Image rotate 90° CW" %>
<% button "image-rotate-ccw.svg" "Image rotate 90° CCW" %>
<% button "image-flip.svg" "Image: flip" %>
<% button "image-mirror.svg" "Image: mirror" %>
</div>
<div class="control col-6 col-lg-2">
<div class="row">
<div class="col-4"><input type="range" orient="vertical" id="isp-again" title="aGain"></div>
<div class="col-4"><input type="range" orient="vertical" id="isp-dgain" title="dGain"></div>
<div class="col-4"><input type="range" orient="vertical" id="isp-gain" title="Gain"></div>
</div>
</div>
<div class="control col-lg-4">
<% button "preset-home.svg" "Preset: Home" %>
<% button "preset-save.svg" "Preset: Save" %>
<% button "preset-1.svg" "Preset 1" %>
<% button "preset-2.svg" "Preset 2" %>
<% button "preset-3.svg" "Preset 3" %>
<% button "preset-4.svg" "Preset 4" %>
<% button "preset-5.svg" "Preset 5" %>
<% button "preset-6.svg" "Preset 6" %>
<% button "preset-7.svg" "Preset 7" %>
<% button "preset-8.svg" "Preset 8" %>
<% button "preset-9.svg" "Preset 9" %>
</div>
</div>
<script>
const ipaddr = '<%= $ipaddr %>';
</script>
<script src="/js/joystick.js"></script>
