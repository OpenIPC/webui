#!/usr/bin/haserl
content-type: text/html

<%
button() {
  img=$1 ; alt=$2
  echo "<li class=\"nav-item\"><a class=\"nav-link\" href=\"\"><img src=\"/img/${img}\" alt=\"${alt}\" width=\"32\" height=\"32\"></a></li>"
}
%>
<%in _header.cgi %>
<h2>Camera preview</h2>

<img id="preview" src="http://<%= $ipaddr %>/image.jpg" alt="" class="img-fluid mb-3" width="1280" height="720">

<ul class="nav nav-pills justify-content-center mb-4">
<% button "arrow-up-square.svg" "Pan up" %>
<% button "arrow-down-square.svg" "Pan down" %>
<% button "arrow-left-square.svg" "Pan left" %>
<% button "arrow-right-square.svg" "Pan right" %>
<% button "dash-square.svg" "Zoom out" %>
<% button "plus-square.svg" "Zoom in" %>
</ul>

<script>
function updatePreview() {
  document.getElementById('preview').src = "http://<%= $ipaddr %>/image.jpg?t=" + Date.now();
  setTimeout(updatePreview, 3500);
}

window.onload = updatePreview;
</script>

<%in _footer.cgi %>
