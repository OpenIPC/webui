#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_system_info
page_title="$tPageTitlePreviewVideo"
%>
<%in _header.cgi %>
<%
div_ "class=\"row preview\""
div_ "class=\"col position-relative mb-4\""
div_ "class=\"ratio ratio-16x9 mb-3\""
%>
<video id="preview" poster="http://<%= $ipaddr %>/image.jpg" autoplay controls>
<source src="http://<%= $ipaddr %>/video.m3u8" type="application/x-mpegURL">
<source src="rtsp://<%= $ipaddr %>/stream=0" type="application/x-rtsp">
<source src="http://<%= $ipaddr %>/video.mp4" type="video/mp4">
<%= $tMsgVideoTagNotSupported %>
</video>
<%
_div
_div
_div
%>
<%in _joystick.cgi %>
<%in _footer.cgi %>
