#!/usr/bin/haserl
<%in _common.cgi %>
<% page_title="Camera Preview"
ipaddr=$(printenv | grep HTTP_HOST | cut -d= -f2 | cut -d: -f1)
button() {
  id=$(echo "${2// /-}" | tr '[:upper:]' '[:lower:]')
  echo "<a id=\"${id}\" href=\"\"><img src=\"/img/${1}\" alt=\"${2}\"></a>"
} %>
<%in _header.cgi %>
<h2>Camera Preview</h2>
<% flash_read %>
<div class="row preview">
  <div class="col position-relative mb-4">
    <div class="ratio ratio-16x9 mb-3">
      <video src="http://<%= $ipaddr %>/video.mp4" poster="http://<%= $ipaddr %>/image.jpg" preload="auto" autoplay controls></video>
    </div>
    <div class="alert alert-danger">Motors not initialized.</div>
    <div class="control">
      <% button "arrow-up-square-fill.svg" "Pan up" %>
      <% button "dash-square-fill.svg" "Zoom out" %>
      <% button "arrow-left-square-fill.svg" "Pan left" %>
      <% button "camera-fill.svg" "Source" %>
      <% button "arrow-right-square-fill.svg" "Pan right" %>
      <% button "arrow-down-square-fill.svg" "Pan down" %>
      <% button "plus-square-fill.svg" "Zoom in" %>
    </div>
  </div>
</div>
<p><a href="/cgi-bin/preview-help.cgi">Camera Available Endpoints cheatsheet</a></p>
<script>
function updateSnapshot() {
  if ($('#snapshot'))
    $('#snapshot').src = "http://<%= $ipaddr %>/image.jpg?t=" + Date.now();
  setTimeout(updateSnapshot, 3500);
}
window.onload = updateSnapshot;
</script>
<%in _footer.cgi %>
