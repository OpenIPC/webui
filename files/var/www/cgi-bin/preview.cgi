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
    <img id="snapshot" src="http://<%= $ipaddr %>/image.jpg" class="img-fluid" width="1280" height="720" alt="">
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
  $('#snapshot').src = "http://<%= $ipaddr %>/image.jpg?t=" + Date.now();
}
$('#snapshot').addEventListener('load', updateSnapshot);
</script>
<%in _footer.cgi %>
