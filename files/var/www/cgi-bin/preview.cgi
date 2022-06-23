#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="$t_preview_0"

size=$(yaml-cli -g .mjpeg.size); [ -z "$size" ] && size="640x480"
size_w=${size%x*}
size_h=${size#*x}
%>
<%in p/header.cgi %>

<div class="row preview">
<div class="col-md-8 col-xl-9 col-xxl-12 position-relative mb-3">
<nav>
<div class="nav nav-tabs" id="nav-tab" role="tablist">
<button class="nav-link active" id="nav-jpeg-tab" data-bs-toggle="tab" data-bs-target="#nav-jpeg" type="button" role="tab" aria-controls="nav-jpeg" aria-selected="true">JPEG</button>
<button class="nav-link" id="nav-mjpeg-tab" data-bs-toggle="tab" data-bs-target="#nav-mjpeg" type="button" role="tab" aria-controls="nav-mjpeg" aria-selected="false">MJPEG</button>
<button class="nav-link" id="nav-video-tab" data-bs-toggle="tab" data-bs-target="#nav-video" type="button" role="tab" aria-controls="nav-video" aria-selected="false">Video</button>
</div>
</nav>
<div class="tab-content" id="nav-tabContent">
<div class="tab-pane fade show active" id="nav-jpeg" role="tabpanel" aria-labelledby="nav-jpeg-tab" tabindex="0">
<div class="ratio ratio-16x9 mb-3">
<img src="http://<%= $ipaddr %>/image.jpg" class="img-fluid" id="preview" width="1280" height="720" alt="">
</div>
</div>
<div class="tab-pane fade" id="nav-mjpeg" role="tabpanel" aria-labelledby="nav-mjpeg-tab" tabindex="0">
<div class="ratio ratio-16x9 mb-3">
<img src="http://<%= $ipaddr %>/mjpeg" class="d-block img-fluid bg-light" height="<%= $size_h %>" width="<%= $size_w %>" alt="<%= $t_preview_5 %>">
<audio autoplay controls class="d-block img-fluid">
<source src="http://<%= $ipaddr %>/audio.opus" type="audio/ogg; codecs=opus">
<source src="http://<%= $ipaddr %>/audio.mp3" type="audio/mpeg">
<%= $t_preview_6 %>
</audio>
</div>
</div>
<div class="tab-pane fade" id="nav-video" role="tabpanel" aria-labelledby="nav-video-tab" tabindex="0">
<div class="ratio ratio-16x9 mb-3">
<video id="preview" poster="http://<%= $ipaddr %>/image.jpg" autoplay class="border">
<source url="http://<%= $ipaddr %>/video.m3u8" type="application/x-mpegURL">
<source url="rtsp://<%= $ipaddr %>/stream=0" type="application/x-rtsp">
<source url="http://<%= $ipaddr %>/video.mp4" type="video/mp4">
<%= $t_preview_7 %>
</video>
</div>
</div>
</div>
</div>
<div class="col-md-4 col-xl-3 col-xxl-12">
<div class="d-grid gap-2 d-md-flex justify-content-md-center mb-3">
<button class="btn btn-primary text-start" type="button" id="preview_night_mode"><%= $t_preview_1 %></button>
<button class="btn btn-primary text-start" type="button" id="send_to_telegram"><%= $t_preview_2 %></button>
<button class="btn btn-primary text-start" type="button" id="send_to_yandex_disk"><%= $t_preview_3 %></button>
</div>
<div class="alert alert-danger">
<%= $t_preview_4 %>
</div>
</div>
</div>

<script src="/a/joystick.js"></script>
<script>
const ipaddr = "<%= $ipaddr %>";
<% if [ ! -f /etc/telegram.cfg ] && [ -z "$(grep telegram_enabled /etc/telegram.cfg | grep true)" ]; then %>
$('#send2telegram').disabled = true;
<% fi %>
<% if [ ! -f /etc/yadisk.cfg ] && [ -z "$(grep yadisk_enabled /etc/yadisk.cfg | grep true)" ]; then %>
$('#send2yadisk').disabled = true;
<% fi %>

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function updatePreview() {
  await sleep(1000);
  $('#preview').src = "http://<%= $ipaddr %>/image.jpg?t=" + Date.now();
}

function initPage() {
  $('#preview').addEventListener('load', updatePreview);
  updatePreview();
}

window.addEventListener('load', initPage);
</script>
<%in p/footer.cgi %>
