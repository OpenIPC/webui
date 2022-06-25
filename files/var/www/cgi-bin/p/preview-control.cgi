#!/usr/bin/haserl

<div class="d-grid gap-2 mb-3">
  <button class="btn btn-primary text-start" type="button" id="preview_night_mode"><%= $t_preview_1 %></button>
  <button class="btn btn-primary text-start" type="button" id="send-to-telegram"><%= $t_preview_2 %></button>
  <button class="btn btn-primary text-start" type="button" id="send-to-yadisk"><%= $t_preview_3 %></button>
</div>
<div class="alert alert-danger">
  <%= $t_preview_4 %>
</div>

<script>
const ipaddr = "<%= $ipaddr %>";
<%
[ ! -f /etc/telegram.cfg ] && [ -z "$(grep telegram_enabled /etc/telegram.cfg | grep true)" ] && echo "$('#send-to-telegram').disabled = true;"
[ ! -f /etc/yadisk.cfg ] && [ -z "$(grep yadisk_enabled /etc/yadisk.cfg | grep true)" ] && echo "$('#send-to-yadisk').disabled = true;"
%>
</script>
<script src="/a/joystick.js"></script>
