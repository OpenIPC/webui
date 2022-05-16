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
<img src="http://<%= $ipaddr %>/mjpeg" class="img-fluid" width="<%= $size_w %>" height="<%= $size_h %>" alt="MJPEG Preview">
<audio autoplay controls style="width:<%= $size_w %>px" class="d-block img-fluid">
<source src="http://<%= $ipaddr %>/audio.opus" type="audio/ogg; codecs=opus">
<source src="http://<%= $ipaddr %>/audio.mp3" type="audio/mpeg">
Your browser does not support the audio element.
</audio>
</div>
</div>
<%in _joystick.cgi %>
<%in _footer.cgi %>
