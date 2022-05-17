#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_system_info
page_title="$tPageTitlePreviewMjpeg"
size=$(yaml-cli -g .mjpeg.size)
[ -z "$size" ] && size="640x480"
size_w=${size%x*}; size_h=${size#*x} %>
<%in _header.cgi %>
<div class="row preview">
<div class="col mb-4">
<img src="http://<%= $ipaddr %>/mjpeg" class="d-block img-fluid bg-light" alt="<%= $tAltMjpegPreview %>" style="height:<%= $size_h %>px;width:<%= $size_w %>px">
<audio autoplay controls style="width:<%= $size_w %>px" class="d-block img-fluid">
<source src="http://<%= $ipaddr %>/audio.opus" type="audio/ogg; codecs=opus">
<source src="http://<%= $ipaddr %>/audio.mp3" type="audio/mpeg">
<%= tMsgAudioTagNotSupported %>
</audio>
</div>
</div>
<%in _joystick.cgi %>
<%in _footer.cgi %>
