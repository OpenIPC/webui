#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_system_info
page_title="$tPageTitlePreviewVideo"
%>
<%in _header.cgi %>
<%
row_ "preview"
  col_ "position-relative mb-4"
    div_ "class=\"ratio ratio-16x9 mb-3\""
      video_ "id=\"preview\" poster=\"http://${ipaddr}/image.jpg\""
        video_source "http://${ipaddr}/video.m3u8" "application/x-mpegURL"
        video_source "rtsp://${ipaddr}/stream=0" "application/x-rtsp"
        video_source "http://${ipaddr}/video.mp4" "video/mp4"
        echo "$tMsgVideoTagNotSupported"
      _video
    _div
  _col
_row
%>
<%in _joystick.cgi %>
<%in _footer.cgi %>
