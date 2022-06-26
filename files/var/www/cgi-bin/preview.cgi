#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Camera preview"

t_preview_1="Toggle night mode"
t_preview_2="Send to Telegram"
t_preview_3="Send to Yandex Disk"
t_preview_5="MJPEG Preview. If you don't see it, it's not supported by your browser, or MJPEG steam does not work."
t_preview_7="Your browser does not support HTML5 video."

size=$(yaml-cli -g .mjpeg.size); [ -z "$size" ] && size="640x480"
size_w=${size%x*}
size_h=${size#*x}
%>
<%in p/header.cgi %>

<div class="row preview">
  <div class="col-md-8 col-xl-9 col-xxl-9 position-relative mb-3">

    <ul class="nav nav-tabs" role="tablist">
      <li class="nav-item" role="presentation">
        <button role="tab" class="nav-link active" data-bs-toggle="tab" data-bs-target="#jpeg-tab-pane" id="jpeg-tab" aria-controls="jpeg-tab-pane" aria-selected="true">JPEG</button>
      </li>
      <li class="nav-item" role="presentation">
        <button role="tab" class="nav-link" data-bs-toggle="tab" data-bs-target="#mjpeg-tab-pane" id="mjpeg-tab" aria-controls="mjpeg-tab-pane" aria-selected="false">MJPEG</button>
      </li>
      <li class="nav-item" role="presentation">
        <button role="tab" class="nav-link" data-bs-toggle="tab" data-bs-target="#video-tab-pane" id="video-tab" aria-controls="video-tab-pane" aria-selected="false">Video</button>
      </li>
    </ul>

    <div class="tab-content p-2" id="tab-content">
      <div id="jpeg-tab-pane" role="tabpanel" class="tab-pane fade show active" aria-labelledby="jpeg-tab" tabindex="0">
        <div class="ratio ratio-16x9">
          <img src="http://<%= $ipaddr %>/image.jpg" class="img-fluid" id="preview-jpeg" width="1280" height="720" alt="">
        </div>
      </div>
      <div id="mjpeg-tab-pane" role="tabpanel" class="tab-pane fade" aria-labelledby="mjpeg-tab" tabindex="0">
        <div class="ratio ratio-16x9">
          <img src="http://<%= $ipaddr %>/mjpeg" class="d-block img-fluid bg-light" height="<%= $size_h %>" width="<%= $size_w %>" alt="<%= $t_preview_5 %>">
          <% if [ "true" = "$(yaml-cli -g .audio.enabled)" ]; then %>
            <audio autoplay controls class="d-block img-fluid">
              <source src="http://<%= $ipaddr %>/audio.opus" type="audio/ogg; codecs=opus">
              <source src="http://<%= $ipaddr %>/audio.m4a" type="audio/aac">
              <source src="http://<%= $ipaddr %>/audio.mp3" type="audio/mpeg">
              Your browser does not support HTML5 audio.
            </audio>
          <% fi %>
        </div>
      </div>
      <div id="video-tab-pane" role="tabpanel" class="tab-pane fade" aria-labelledby="video-tab" tabindex="0">
        <div class="ratio ratio-16x9">
          <video id="preview-video" poster="http://<%= $ipaddr %>/image.jpg" autoplay>
            <source src="http://<%= $ipaddr %>/video.mp4" type="video/mp4">
            <%= $t_preview_7 %>
          </video>
        </div>
      </div>
    </div>
  </div>
  <div class="col-md-4 col-xl-3 col-xxl-3 pt-5">
    <div class="d-grid gap-2 mb-3">
      <div class="input-group">
        <button class="form-control btn btn-primary text-start" type="button" id="preview_night_mode"><%= $t_preview_1 %></button>
      </div>
      <div class="input-group">
        <button class="form-control btn btn-primary text-start" type="button" id="send-to-telegram"><%= $t_preview_2 %></button>
        <div class="input-group-text">
          <a href="/cgi-bin/plugin-telegram.cgi" title="Telegram bot settings"><img src="/a/gear.svg" alt="Gear"></a>
        </div>
      </div>
      <div class="input-group">
        <button class="form-control btn btn-primary text-start" type="button" id="send-to-yadisk"><%= $t_preview_3 %></button>
        <div class="input-group-text">
          <a href="/cgi-bin/plugin-yadisk.cgi" title="Yandex Disk bot settings"><img src="/a/gear.svg" alt="Gear"></a>
        </div>
      </div>
    </div>

    <div class="alert alert-danger small">
      PTZ feature is not ready. Please consider <a href="https://t.me/OpenIPC">supporting further development</a>.
    </div>
  </div>
</div>

<script>
const ipaddr = "<%= $ipaddr %>";

<% [ "true" != "$telegram_enabled" ] && echo "\$('#send-to-telegram').disabled = true;" %>
<% [ "true" != "$yadisk_enabled" ] && echo "\$('#send-to-yadisk').disabled = true;" %>

function reqListener() {
    console.log(this.responseText);
}

function sendToApi(endpoint) {
    const xhr = new XMLHttpRequest();
    xhr.addEventListener("load", reqListener);
    xhr.open("GET", "http://" + ipaddr + endpoint);
    xhr.setRequestHeader("Authorization", "Basic " + btoa("admin:"));
    xhr.send();
}

function initControls() {
    $$("a[id^=pan-],a[id^=zoom-]").forEach(el => {
        el.addEventListener("click", event => {
            event.preventDefault();
            alert("Sorry, this feature does not work, yet!");
        });
    });

    $("#night-mode")?.addEventListener("click", event => {
        event.preventDefault();
        event.target.src = (event.target.src.split("/").pop() == "light-on.svg") ? "/a/light-off.svg" : "/a/light-on.svg";
        // sendToApi("/night/toggle");
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/cgi-bin/night.cgi");
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.send("mode=toggle");
    });

    $("#speed")?.addEventListener("click", event => {
        event.preventDefault();
        event.target.src = (event.target.src.split("/").pop() == "speed-slow.svg") ? "/a/speed-fast.svg" : "/a/speed-slow.svg";
        // sendToApi("/speed/toggle");
    });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function updatePreview() {
  await sleep(1000);
  $('#preview-jpeg').src = "http://<%= $ipaddr %>/image.jpg?t=" + Date.now();
}

$('#preview-jpeg').addEventListener('load', updatePreview);
updatePreview();
initControls();
</script>

<%in p/footer.cgi %>
