#!/usr/bin/haserl
<%
#button() {
#  id=$(echo "${2// /-}" | tr '[:upper:]' '[:lower:]' | tr -cd '[:alnum:]-' )
#  echo "<a href=\"\" class=\"btn btn-primary\">"
#  echo "<img id=\"${id}\" src=\"/a/${1}\" alt=\"${2}\" title=\"${2}\">"
#  echo "${2}"
#  echo "</a>"
#}

#row_ "control-board"
#  col_ "control"
#    button "arrow-ul.svg" "Pan up left"
#    button "arrow-uc.svg" "Pan up"
#    button "arrow-ur.svg" "Pan up right"
#    button "arrow-cl.svg" "Pan left"
#    button "arrow-cr.svg" "Pan right"
#    button "arrow-dl.svg" "Pan down left"
#    button "arrow-dc.svg" "Pan down"
#    button "arrow-dr.svg" "Pan down right"
#    button "speed-slow.svg" "Speed"
#    button "zoom-close.svg" "Zoom in"
#    button "zoom-far.svg" "Zoom out"
#    button "focus-plus.svg" "Focus: plus"
#    button "focus-auto.svg" "Focus: auto"
#    button "focus-minus.svg" "Focus: minus"
# [ "true" = "$(yaml-cli -g .nightMode.enabled)" ] &&
#_col

#  col_ "col-6 col-lg-2 control"
#    button "image-rotate-cw.svg" "Image rotate 90° CW"
#    button "image-rotate-ccw.svg" "Image rotate 90° CCW"
#    button "image-flip.svg" "Image: flip"
#    button "image-mirror.svg" "Image: mirror"
#  _col

#  col_ "col-6 col-lg-2 control"
#    row_
#      div "<input type=\"range\" orient=\"vertical\" id=\"isp-again\" title=\"aGain\">" "col-4"
#      div "<input type=\"range\" orient=\"vertical\" id=\"isp-dgain\" title=\"dGain\">" "col-4"
#      div "<input type=\"range\" orient=\"vertical\" id=\"isp-gain\" title=\"Gain\">" "col-4"
#    _row
#  _col

#  col_ "col-lg-4 control"
#    button "preset-home.svg" "Preset: Home"
#    button "preset-save.svg" "Preset: Save"
#    button "preset-1.svg" "Preset 1"
#    button "preset-2.svg" "Preset 2"
#    button "preset-3.svg" "Preset 3"
#    button "preset-4.svg" "Preset 4"
#    button "preset-5.svg" "Preset 5"
#    button "preset-6.svg" "Preset 6"
#    button "preset-7.svg" "Preset 7"
#    button "preset-8.svg" "Preset 8"
#    button "preset-9.svg" "Preset 9"
#  _col
#_row
#button "light-off.svg" "Night mode"
#button "telegram.svg" "Send to Telegram"
%>

<div class="d-grid gap-2 mb-3">
  <button class="btn btn-primary text-start" type="button" id="preview_night_mode"><%= $t_preview_1 %></button>
  <button class="btn btn-primary text-start" type="button" id="send_to_telegram"><%= $t_preview_2 %></button>
  <button class="btn btn-primary text-start" type="button" id="send_to_yandex_disk"><%= $t_preview_3 %></button>
</div>

<div class="alert alert-danger">
  <%= $t_preview_4 %>
</div>

<script>
const ipaddr = "<%= $ipaddr %>";
<% if [ ! -f /etc/telegram.cfg ] && [ -z "$(grep telegram_enabled /etc/telegram.cfg | grep true)" ]; then %>
$('#send2telegram').disabled = true;
<% fi %>
<% if [ ! -f /etc/yadisk.cfg ] && [ -z "$(grep yadisk_enabled /etc/yadisk.cfg | grep true)" ]; then %>
$('#send2yadisk').disabled = true;
<% fi %>
</script>
<script src="/a/joystick.js"></script>
