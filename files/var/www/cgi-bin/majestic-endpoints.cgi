#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Majestic Endpoints"
%>
<%in p/header.cgi %>
<div class="row row-cols-1 row-cols-md-2 row-cols-xl-3 g-4 mb-4">
  <div class="col">
    <h3>Video</h3>
    <dl>
      <dt class="cp2cb">http://<%= $network_address %>/mjpeg</dt>
      <dd>MJPEG video stream.</dd>
      <dt class="cp2cb">http://<%= $network_address %>/video.mp4</dt>
      <dd>fMP4 video stream.</dd>
      <dt class="cp2cb">rtsp://username:password@<%= $network_address %>/stream=0</dt>
      <dd>RTSP main stream (video0).</dd>
      <dt class="cp2cb">rtsp://username:password@<%= $network_address %>/stream=1</dt>
      <dd>RTSP substream (video1).</dd>
      <dt class="cp2cb">http://<%= $network_address %>/hls</dt>
      <dd>HLS live-streaming in web browser.</dd>
      <dt class="cp2cb">http://<%= $network_address %>/webrtc</dt>
      <dd>WebRTC live-streaming in web browser.</dd>
      <dt class="cp2cb">http://<%= $network_address %>/mjpeg.html</dt>
      <dd>MJPEG &amp; MP3 live-streaming in web browser.</dd>
    </dl>
  </div>
  <div class="col">
    <h3>Audio</h3>
    <dl>
      <dt class="cp2cb">http://<%= $network_address %>/audio.opus</dt>
      <dd>Opus audio stream.</dd>
      <dt class="cp2cb">http://<%= $network_address %>/audio.pcm</dt>
      <dd>Raw PCM audio stream.</dd>
      <dt class="cp2cb">http://<%= $network_address %>/audio.m4a</dt>
      <dd>AAC audio stream.</dd>
      <dt class="cp2cb ult">http://<%= $network_address %>/audio.mp3</dt>
      <dd class="ult">MP3 audio stream.</dd>
      <dt class="cp2cb">http://<%= $network_address %>/audio.alaw</dt>
      <dd>A-law compressed audio stream.</dd>
      <dt class="cp2cb">http://<%= $network_address %>/audio.ulaw</dt>
      <dd>μ-law compressed audio stream.</dd>
      <dt class="cp2cb">http://<%= $network_address %>/audio.g711a</dt>
      <dd>G.711 A-law audio stream.</dd>
      <dt class="cp2cb">http://<%= $network_address %>/play_audio</dt>
      <dd>Play audio file on camera&#39;s speaker.<sup>1,3</sup>
        <div class="small">Accepts POST requests with audio file as a parameter.</div></dd>
    </dl>
  </div>
  <div class="col">
    <h3>Still Images</h3>
    <dl>
      <dt class="cp2cb">http://<%= $network_address %>/image.jpg</dt>
      <dd>Snapshot in JPEG format.<br>Optional parameters:<sup>2,4</sup>
        <ul class="small">
          <li>width, height - size of resulting image</li>
          <li>qfactor - JPEG quality factor (1-99)</li>
          <li>color2gray - convert to grayscale</li>
          <li>crop - crop resulting image as 16x16x320x320</li>
        </ul>
      </dd>
      <dt class="cp2cb">http://<%= $network_address %>/image.heif</dt>
      <dd>Snapshot in HEIF format.</dd>
      <dt class="cp2cb">http://<%= $network_address %>/image.yuv420</dt>
      <dd>Snapshot in YUV420 format.</dd>
      <dt class="cp2cb">http://<%= $network_address %>/image.dng</dt>
      <dd>Snapshot in Adobe DNG format (raw).<sup>3</sup></dd>
    </dl>
  </div>
  <div class="col">
    <h3>Night API</h3>
    <dl>
      <dt class="cp2cb">http://<%= $network_address %>/night/on</dt>
      <dd>Turn on night mode.</dd>
      <dt class="cp2cb">http://<%= $network_address %>/night/off</dt>
      <dd>Turn off night mode.</dd>
      <dt class="cp2cb">http://<%= $network_address %>/night/toggle</dt>
      <dd>Toggle current night mode.</dd>
    </dl>
  </div>
  <div class="col">
    <h3>Monitoring</h3>
    <dl>
      <dt class="cp2cb">http://<%= $network_address %>/api/v1/config.json</dt>
      <dd>Actual Majestic config in JSON format.</dd>
      <dt class="cp2cb">http://<%= $network_address %>/metrics</dt>
      <dd>Node exporter for <a href="https://prometheus.io/">Prometheus</a>.</dd>
    </dl>
  </div>
</div>

<ol class="footnotes small">
  <li class="text-body-secondary">Only HiSilicon and Goke SoCs.</li>
  <li class="text-body-secondary">Only HiSilicon SoCs v2 and up.</li>
  <li class="text-body-secondary">E.g. <i>ffplay -ar 48000 -ac 1 -f s16le http://<%= $network_address %>/audio.pcm</i></li>
  <li class="text-body-secondary">E.g. <i>http://<%= $network_address %>/image.jpg?width=640&height=480&qfactor=50&color2gray=1&crop=80x32x512x400</i></li>
</ol>

<p class="text-body-secondary">More examples available <a href="https://github.com/OpenIPC/wiki/blob/master/en/majestic-streamer.md">in our wiki</a>.</p>

<script>
    function initializeCopyToClipboard() {
        document.querySelectorAll(".cp2cb").forEach(function (element) {
            element.title = "Click to copy to clipboard";

            element.addEventListener("click", function (event) {
                event.target.preventDefault;
                event.target.animate({ color: 'red' }, 500);

                if (navigator.clipboard && window.isSecureContext) {
                    navigator.clipboard.writeText(event.target.textContent).then(r => playChime(r));
                } else {
                    let textArea = document.createElement("textarea");
                    textArea.value = event.target.textContent;
                    textArea.style.position = "fixed";
                    textArea.style.left = "-999999px";
                    textArea.style.top = "-999999px";
                    document.body.appendChild(textArea);
                    textArea.focus();
                    textArea.select();
                    return new Promise((res, rej) => {
                        document.execCommand('copy') ? res() : rej();
                        textArea.remove();
                    });
                }
            })
        })
    }
    window.onload = function () {
        initializeCopyToClipboard();
    }
</script>
<%in p/footer.cgi %>
