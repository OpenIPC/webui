#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_system_info
page_title="$tPageTitlePreviewHelp"
%>
<%in _header.cgi %>
<%
p "Detailed information available $(link_to "in the wiki" "https://github.com/OpenIPC/wiki/blob/master/en/majestic-streamer.md")."

div_ "class=\"row row-cols-1 row-cols-md-2 row-cols-xl-3 g-3\""
  col_card_ "Web Pages"
    dl_
      dt "http://${ipaddr}/"
      dd "HLS live streaming is web browser."
      dt "http://${ipaddr}/mjpeg.html"
      dd "MJPEG & MP3 live streaming in web browser."
    _dl
  _col_card

  col_card_ "Video Streams"
    dl_
      dt "http://${ipaddr}/mjpeg"
      dd "MJPEG video stream."
      dt "http://${ipaddr}/video.mp4"
      dd "fMP4 video stream."
      dt "rtsp://${ipaddr}/stream=0"
      dd "RTSP primary stream (video0)."
      dt "rtsp://${ipaddr}/stream=1"
      dd "RTSP secondary stream (video1)."
    _dl
  _col_card

  col_card_ "Still Images"
    dl_
      dt "http://${ipaddr}/image.jpg"
      dd "Snapshot in JPEG format.<br>
        Optional parameters:
        <ul class="small">
          <li>width, height - size of resulting image</li>
          <li>qfactor - JPEG quality factor (1-99)</li>
          <li>color2gray - convert to grayscale</li>
          <li>crop - crop resulting image as 16x16x320x320</li>
        </ul>"
      dt "http://${ipaddr}/image.heif"
      dd "Snapshot in HEIF format."
      dt "http://${ipaddr}/image.yuv420"
      dd "Snapshot in YUV420 format"
      dt "http://${ipaddr}/image.dng"
      dd "Snapshot in Adobe DNG format (raw)<br>(only for v>=2 HiSilicon processors)."
    _dl
  _col_card

  col_card_ "Audio Streams"
    dl_
      dt "http://${ipaddr}/audio.opus"
      dd "Opus audio stream."
      dt "http://${ipaddr}/audio.pcm"
      dd "Raw PCM audio stream."
      dt "http://${ipaddr}/audio.m4a"
      dd "AAC audio stream."
      dt "http://${ipaddr}/audio.mp3"
      dd "MP3 audio stream."
      dt "http://${ipaddr}/audio.alaw"
      dd "A-law compressed audio stream."
      dt "http://${ipaddr}/audio.ulaw"
      dd "μ-law compressed audio stream."
      dt "http://${ipaddr}/audio.g711a"
      dd "G.711 A-law audio stream."
    _dl
  _col_card

  col_card_ "Night API"
    dl_
      dt "http://${ipaddr}/night/on"
      dd "Turn on night mode."
      dt "http://${ipaddr}/night/off"
      dd "Turn off night mode."
      dt "http://${ipaddr}/night/toggle"
      dd "Toggle current night mode."
    _dl
  _col_card

  col_card_ "Monitoring"
    dl_
      dt "http://${ipaddr}/metrics"
      dd "Standard Node exporter compatible and application-specific metrics for Prometheus."
    _dl
  _col_card
_div
%>
<%in _footer.cgi %>
