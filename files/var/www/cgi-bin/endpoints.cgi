#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="Available endpoints" %>
<%in p/header.cgi %>

<p>Detailed information available <a href="https://github.com/OpenIPC/wiki/blob/master/en/majestic-streamer.md">in the wiki</a>.</p>

<div class="row row-cols-1 row-cols-md-2 row-cols-xl-3 g-4">
  <div class="col">
    <h3>Web Pages</h3>
    <dl>
      <dt>http://<%= $ipaddr %>/</dt>
      <dd>HLS live-streaming in web browser.</dd>
      <dt>http://<%= $ipaddr %>/mjpeg.html</dt>
      <dd>MJPEG & MP3 live-streaming in web browser.</dd>
    </dl>
  </div>
  <div class="col">
    <h3>Video Streams</h3>
    <dl>
      <dt>http://<%= $ipaddr %>/mjpeg</dt>
      <dd>MJPEG video stream.</dd>
      <dt>http://<%= $ipaddr %>/video.mp4</dt>
      <dd>fMP4 video stream.</dd>
      <dt>rtsp://<%= $ipaddr %>/stream=0</dt>
      <dd>RTSP primary stream (video0).</dd>
      <dt>rtsp://<%= $ipaddr %>/stream=1</dt>
      <dd>RTSP secondary stream (video1).</dd>
    </dl>
  </div>
  <div class="col">
    <h3>Still Images</h3>
    <dl>
      <dt>http://<%= $ipaddr %>/image.jpg</dt>
      <dd>Snapshot in JPEG format.<br>Optional parameters:
        <ul class="small">
          <li>width, height - size of resulting image</li>
          <li>qfactor - JPEG quality factor (1-99)</li>
          <li>color2gray - convert to grayscale</li>
          <li>crop - crop resulting image as 16x16x320x320</li>
        </ul>
      </dd>
      <dt>http://<%= $ipaddr %>/image.heif</dt>
      <dd>Snapshot in HEIF format.</dd>
      <dt>http://<%= $ipaddr %>/image.yuv420</dt>
      <dd>Snapshot in YUV420 format.</dd>
      <dt>http://<%= $ipaddr %>/image.dng</dt>
      <dd>Snapshot in Adobe DNG format (raw)<br>(only for HiSilicon processors v>=2).</dd>
    </dl>
  </div>
  <div class="col">
    <h3>Audio Streams</h3>
    <dl>
      <dt>http://<%= $ipaddr %>/audio.opus</dt>
      <dd>Opus audio stream.</dd>
      <dt>http://<%= $ipaddr %>/audio.pcm</dt>
      <dd>Raw PCM audio stream.</dd>
      <dt>http://<%= $ipaddr %>/audio.m4a</dt>
      <dd>AAC audio stream.</dd>
      <dt class="ult">http://<%= $ipaddr %>/audio.mp3</dt>
      <dd class="ult">MP3 audio stream.</dd>
      <dt>http://<%= $ipaddr %>/audio.alaw</dt>
      <dd>A-law compressed audio stream.</dd>
      <dt>http://<%= $ipaddr %>/audio.ulaw</dt>
      <dd>μ-law compressed audio stream.</dd>
      <dt>http://<%= $ipaddr %>/audio.g711a</dt>
      <dd>G.711 A-law audio stream.</dd>
    </dl>
  </div>
  <div class="col">
    <h3>Night API</h3>
    <dl>
      <dt>http://<%= $ipaddr %>/night/on</dt>
      <dd>Turn on night mode.</dd>
      <dt>http://<%= $ipaddr %>/night/off</dt>
      <dd>Turn off night mode.</dd>
      <dt>http://<%= $ipaddr %>/night/toggle</dt>
      <dd>Toggle current night mode.</dd>
    </dl>
  </div>
  <div class="col">
    <h3>Monitoring</h3>
    <dl>
      <dt>http://<%= $ipaddr %>/metrics</dt>
      <dd>Standard Node exporter compatible and application-specific metrics for Prometheus.</dd>
    </dl>
  </div>
</div>

<%in p/footer.cgi %>
