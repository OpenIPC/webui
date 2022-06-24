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
  <div class="col-md-8 col-xl-9 col-xxl-10 position-relative mb-3">
    <nav role="tablist" id="tab-nav">
      <a id="nav-jpeg-tab">JPEG</a>
      <a id="nav-mjpeg-tab">MJPEG</a>
      <a id="nav-video-tab">Video</a>
    </nav>
    <div class="tab-content p-2" id="tab-content">
      <div id="jpeg-tab-pane" role="tabpanel">
        <div class="ratio ratio-16x9">
          <img src="http://<%= $ipaddr %>/image.jpg" class="img-fluid" id="preview" width="1280" height="720" alt="">
        </div>
      </div>
      <div id="mjpeg-tab-pane" role="tabpanel">
        <div class="ratio ratio-16x9">
          <img src="http://<%= $ipaddr %>/mjpeg" class="d-block img-fluid bg-light" height="<%= $size_h %>" width="<%= $size_w %>" alt="<%= $t_preview_5 %>">
          <audio autoplay controls class="d-block img-fluid">
            <source src="http://<%= $ipaddr %>/audio.opus" type="audio/ogg; codecs=opus">
            <source src="http://<%= $ipaddr %>/audio.mp3" type="audio/mpeg">
            <%= $t_preview_6 %>
          </audio>
        </div>
      </div>
      <div id="video-tab-pane" role="tabpanel">
        <div class="ratio ratio-16x9">
          <video id="preview" poster="http://<%= $ipaddr %>/image.jpg" autoplay>
          <source url="http://<%= $ipaddr %>/video.m3u8" type="application/x-mpegURL">
          <source url="rtsp://<%= $ipaddr %>/stream=0" type="application/x-rtsp">
          <source url="http://<%= $ipaddr %>/video.mp4" type="video/mp4">
          <%= $t_preview_7 %>
        </video>
        </div>
      </div>
    </div>
  </div>
  <div class="col-md-4 col-xl-3 col-xxl-2 pt-5">
    <div class="d-grid gap-2 mb-3">
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
