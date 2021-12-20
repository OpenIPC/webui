#!/usr/bin/haserl
<%in _common.cgi %>
<% page_title="Video Preview"
ipaddr=$(printenv | grep HTTP_HOST | cut -d= -f2 | cut -d: -f1)
%>
<%in _header.cgi %>
<div class="row preview">
  <div class="col position-relative mb-4">
    <div class="ratio ratio-16x9 mb-3">
      <video id="preview" poster="http://<%= $ipaddr %>/image.jpg" autoplay controls>
        <source src="http://<%= $ipaddr %>/video.m3u8" type="application/x-mpegURL">
        <source src="rtsp://<%= $ipaddr %>/stream=0" type="application/x-rtsp">
        <source src="http://<%= $ipaddr %>/video.mp4" type="video/mp4">
      </video>
    </div>
  </div>
</div>
<%in _joystick.cgi %>
<p><a href="/cgi-bin/preview-help.cgi">Camera Available Endpoints cheatsheet</a></p>
<%in _footer.cgi %>
