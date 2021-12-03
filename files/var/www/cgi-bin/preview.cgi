#!/usr/bin/haserl
content-type: text/html

<% ipaddr=$(printenv | grep HTTP_HOST | cut -d= -f2 | cut -d: -f1) %>
<%in _header.cgi %>
<h2>Camera preview</h2>

<img id="preview" src="http://<%= $ipaddr %>/image.jpg" alt="" class="img-fluid border" width="1600" height="900">

<ul class="nav nav-pills justify-content-center">
 <li class="nav-item"><a class="nav-link" href="">🡄</a></li>
 <li class="nav-item"><a class="nav-link" href="">🡆</a></li>
 <li class="nav-item"><a class="nav-link" href="">🡅</a></li>
 <li class="nav-item"><a class="nav-link" href="">🡇</a></li>
 <li class="nav-item"><a class="nav-link" href="">+</a></li>
 <li class="nav-item"><a class="nav-link" href="">-</a></li>
</ul>

<script>
function updatePreview() {
  let img = new Image();
  img.src = "http://<%= $ipaddr %>/image.jpg?" + Date.now();
  img.addEventListener('ready', () => document.getElementById('preview').src = img.src);
  setTimeout(updatePreview, 3500);
}
window.onload = updatePreview;
</script>

<%in _footer.cgi %>
