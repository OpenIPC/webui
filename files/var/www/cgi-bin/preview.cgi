#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Camera preview"

size=$(yaml-cli -g .mjpeg.size); [ -z "$size" ] && size="640x480"
size_w=${size%x*}
size_h=${size#*x}
%>
<%in p/header.cgi %>

<div class="row preview">
  <div class="col-md-8 col-xl-9 col-xxl-9 position-relative mb-3">
    <ul class="nav nav-tabs" role="tablist">
      <% tab_lap "jpeg" "JPEG" "active" %>
      <% tab_lap "mjpeg" "MJPEG" %>
      <% tab_lap "video" "Video" %>
    </ul>
    <div class="tab-content p-2" id="tab-content">
      <div id="jpeg-tab-pane" role="tabpanel" class="tab-pane fade active show" aria-labelledby="jpeg-tab" tabindex="0">
        <% preview 1 %>
      </div>
      <div id="mjpeg-tab-pane" role="tabpanel" class="tab-pane fade" aria-labelledby="mjpeg-tab" tabindex="0">
        <div class="ratio ratio-16x9">
          <% if [ "true" = "$(yaml-cli -g .jpeg.enabled)" ]; then %>
            <img src="http://<%= $network_address %>/image.jpg" class="d-block img-fluid bg-light" id="preview-mjpeg" height="<%= $size_h %>" width="<%= $size_w %>" alt="MJPEG Preview. If you don't see it, it's not supported by your browser, or MJPEG steam does not work.">
          <% else %>
            <p class="alert alert-warning"><a href="majestic-settings.cgi?tab=jpeg">Enable JPEG support</a> to see the preview.</p>
          <% fi %>
          <% if [ "true" = "$(yaml-cli -g .audio.enabled)" ]; then %>
            <audio autoplay controls class="d-block img-fluid">
              <source src="http://<%= $network_address %>/audio.opus" type="audio/ogg; codecs=opus">
              <source src="http://<%= $network_address %>/audio.m4a" type="audio/aac">
              <source src="http://<%= $network_address %>/audio.mp3" type="audio/mpeg">
              Your browser does not support HTML5 audio.
            </audio>
          <% fi %>
        </div>
      </div>
      <div id="video-tab-pane" role="tabpanel" class="tab-pane fade" aria-labelledby="video-tab" tabindex="0">
        <div class="ratio ratio-16x9">
          <video id="preview-video" poster="http://<%= $network_address %>/image.jpg" autoplay>
            <source src="http://<%= $network_address %>/video.mp4" type="video/mp4">
            Your browser does not support HTML5 video.
          </video>
        </div>
      </div>
    </div>
  </div>
  <div class="col-md-4 col-xl-3 col-xxl-3 pt-5">
    <div class="d-grid gap-2 mb-3">
      <div class="input-group">
        <button class="form-control btn btn-primary text-start" type="button" id="toggle-night-mode">Toggle night mode</button>
        <div class="input-group-text">
          <img src="/a/light-off.svg" alt="Image: Night mode indicator" id="night-mode-status">
        </div>
      </div>
      <div class="input-group">
        <button class="form-control btn btn-primary text-start" type="button" id="send-to-email">Send to email</button>
        <div class="input-group-text">
          <a href="plugin-send2email.cgi" title="Email settings"><img src="/a/gear.svg" alt="Gear"></a>
        </div>
      </div>
      <div class="input-group">
        <button class="form-control btn btn-primary text-start" type="button" id="send-to-ftp">Send to FTP</button>
        <div class="input-group-text">
          <a href="plugin-send2ftp.cgi" title="FTP Storage settings"><img src="/a/gear.svg" alt="Gear"></a>
        </div>
      </div>
      <div class="input-group">
        <button class="form-control btn btn-primary text-start" type="button" id="send-to-telegram">Send to Telegram</button>
        <div class="input-group-text">
          <a href="plugin-send2telegram.cgi" title="Telegram bot settings"><img src="/a/gear.svg" alt="Gear"></a>
        </div>
      </div>
      <div class="input-group">
        <button class="form-control btn btn-primary text-start" type="button" id="send-to-yadisk">Send to Yandex Disk</button>
        <div class="input-group-text">
          <a href="plugin-send2yadisk.cgi" title="Yandex Disk bot settings"><img src="/a/gear.svg" alt="Gear"></a>
        </div>
      </div>
    </div>
    <div class="alert alert-danger small">
      PTZ feature is not ready. Please consider <a href="https://t.me/OpenIPC">supporting further development</a>.
    </div>
  </div>
</div>

<script>
const network_address = "<%= $network_address %>";

<% [ "true" != "$email_enabled"    ] && echo "\$('#send-to-email').disabled = true;" %>
<% [ "true" != "$ftp_enabled"      ] && echo "\$('#send-to-ftp').disabled = true;" %>
<% [ "true" != "$telegram_enabled" ] && echo "\$('#send-to-telegram').disabled = true;" %>
<% [ "true" != "$yadisk_enabled"   ] && echo "\$('#send-to-yadisk').disabled = true;" %>

function reqListener(data) {
  console.log(data.responseText);
}

function sendToApi(endpoint) {
  const xhr = new XMLHttpRequest();
  xhr.addEventListener("load", reqListener);
  xhr.open("GET", "http://" + network_address + endpoint);
  xhr.setRequestHeader("Authorization", "Basic " + btoa("admin:"));
  xhr.send();
}

$$("a[id^=pan-],a[id^=zoom-]").forEach(el => {
  el.addEventListener("click", event => {
    event.preventDefault();
    alert("Sorry, this feature does not work, yet!");
  });
});

$("#toggle-night-mode")?.addEventListener("click", event => {
  event.preventDefault();
  $('#night-mode-status').src = ($('#night-mode-status').src.split("/").pop() == "light-on.svg") ? "/a/light-off.svg" : "/a/light-on.svg";
  // sendToApi("/night/toggle");
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/cgi-bin/night.cgi");
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhr.send("mode=toggle");
});

$("#send-to-email")?.addEventListener("click", event => {
    event.preventDefault();
    if (!confirm("Are you sure?")) return false;
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/cgi-bin/send2email.cgi");
    xhr.send();
})

$("#send-to-ftp")?.addEventListener("click", event => {
    event.preventDefault();
    if (!confirm("Are you sure?")) return false;
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/cgi-bin/send2ftp.cgi");
    xhr.send();
})

$("#send-to-telegram")?.addEventListener("click", event => {
    event.preventDefault();
    if (!confirm("Are you sure?")) return false;
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/cgi-bin/send2telegram.cgi");
    xhr.send();
});

$("#send-to-yadisk")?.addEventListener("click", event => {
    event.preventDefault();
    if (!confirm("Are you sure?")) return false;
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/cgi-bin/send2yadisk.cgi");
    xhr.send();
});

$("#speed")?.addEventListener("click", event => {
  event.preventDefault();
  event.target.src = (event.target.src.split("/").pop() == "speed-slow.svg") ? "/a/speed-fast.svg" : "/a/speed-slow.svg";
  // sendToApi("/speed/toggle");
});

$$('button[data-bs-toggle=tab]').forEach(el => el.addEventListener('shown.bs.tab', event => {
  if (event.target.id == "#jpeg-tab") {
    $('#preview-jpeg').addEventListener('load', updatePreview);
    updatePreview();
  }
  if (event.target.id == "#mjpeg-tab") {
    $('#preview-mjpeg').src = "http://<%= $network_address %>/mjpeg";
  }

  if (event.relatedTarget) {
    if (event.relatedTarget.id == "#jpeg-tab") {
      $('#preview-jpeg').removeEventListener('load', updatePreview);
    }
    if (event.relatedTarget.id == "#mjpeg-tab") {
      $('#preview-mjpeg').src="http://<%= $network_address %>/image.jpg";
    }
  }
}));
</script>

<%in p/footer.cgi %>
