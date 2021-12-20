#!/usr/bin/haserl
<%
ipaddr=$(printenv | grep HTTP_HOST | cut -d= -f2 | cut -d: -f1)
button() {
  id=$(echo "${2// /-}" | tr '[:upper:]' '[:lower:]')
  echo "<img id=\"${id}\" src=\"/img/${1}\" alt=\"${2}\">"
}
%>
<div class="control">
<% button "arrow-up-left-square-fill.svg" "Pan up left" %>
<% button "arrow-up-square-fill.svg" "Pan up" %>
<% button "arrow-up-right-square-fill.svg" "Pan up right" %>
<% button "dash-square-fill.svg" "Zoom out" %>
<% button "arrow-left-square-fill.svg" "Pan left" %>
<% button "camera-fill.svg" "Source" %>
<% button "arrow-right-square-fill.svg" "Pan right" %>
<% button "arrow-down-left-square-fill.svg" "Pan down left" %>
<% button "arrow-down-square-fill.svg" "Pan down" %>
<% button "arrow-down-right-square-fill.svg" "Pan down right" %>
<% button "plus-square-fill.svg" "Zoom in" %>
<% [ "true" = "$(yaml-cli -g .nightMode.enabled)" ] && [ "true" = "$(yaml-cli -g .nightMode.nightAPI)" ] && button "lightbulb-off-fill.svg" "Night mode" %>
</div>

<script>
function reqListener() {
  console.log(this.responseText);
}

function initControls() {
  $$('a[id^=pan-],a[id^=zoom-]').forEach(el => {
    el.style.backgroundColor = 'red';
    el.addEventListener('click', event => {
      event.preventDefault();
      alert('Sorry, this feature does not work, yet!');
    });
  });

  if ($('#night-mode')) $('#night-mode').addEventListener('click', event => {
    event.preventDefault();
    const xhr = new XMLHttpRequest();
    xhr.addEventListener("load", reqListener);
    xhr.open("GET", "http://<%= $ipaddr %>/night/toggle");
    xhr.send();
  });
}

window.addEventListener('load', initControls);
</script>
