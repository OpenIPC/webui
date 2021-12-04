#!/usr/bin/haserl
content-type: text/html

<% ipaddr=$(printenv | grep HTTP_HOST | cut -d= -f2 | cut -d: -f1) %>
<%in _header.cgi %>
<h2>Camera preview</h2>

<img id="preview" src="http://<%= $ipaddr %>/image.jpg" alt="" class="img-fluid mb-3" width="1280" height="720">

<ul class="nav nav-pills justify-content-center">
 <li class="nav-item"><a class="nav-link" href=""><img src="/img/arrow-up-square.svg" alt="Pan up" width="32" height="32"></a></li>
 <li class="nav-item"><a class="nav-link" href=""><img src="/img/arrow-down-square.svg" alt="Pan down" width="32" height="32"></i></a></li>
 <li class="nav-item"><a class="nav-link" href=""><img src="/img/arrow-left-square.svg" alt="Pan left" width="32" height="32"></a></li>
 <li class="nav-item"><a class="nav-link" href=""><img src="/img/arrow-right-square.svg" alt="Pan right" width="32" height="32"></i></a></li>
 <li class="nav-item"><a class="nav-link" href=""><img src="/img/dash-square.svg" alt="Zoom out" width="32" height="32"></a></li>
 <li class="nav-item"><a class="nav-link" href=""><img src="/img/plus-square.svg" alt="Zoom in" width="32" height="32"></a></li>
</ul>

<script>
function updatePreview() {
  document.getElementById('preview').src = "http://<%= $ipaddr %>/image.jpg?t=" + Date.now();
  setTimeout(updatePreview, 3500);
}

window.onload = updatePreview;
</script>

<%in _footer.cgi %>
