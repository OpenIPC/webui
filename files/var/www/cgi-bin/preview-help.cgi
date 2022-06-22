#!/usr/bin/haserl
<%in _common.cgi %>
<% page_title="$t_endpoints_0" %>
<%in _header.cgi %>
<p><%= $t_endpoints_1 %> <a href="https://github.com/OpenIPC/wiki/blob/master/en/majestic-streamer.md"><%= $t_endpoints_2 %></a>.</p>
<div class="row row-cols-1 row-cols-md-2 row-cols-xl-3 g-3">
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_endpoints_3 %></div>
<div class="card-body">
<dl>
<dt>http://<%= $ipaddr %>/</dt>
<dd><%= $t_endpoints_4 %></dd>
<dt>http://<%= $ipaddr %>/mjpeg.html</dt>
<dd><%= $t_endpoints_5 %></dd>
</dl>
</div>
</div>
</div>
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_endpoints_6 %></div>
<div class="card-body">
<dl>
<dt>http://<%= $ipaddr %>/mjpeg</dt>
<dd><%= $t_endpoints_7 %></dd>
<dt>http://<%= $ipaddr %>/video.mp4</dt>
<dd><%= $t_endpoints_8 %></dd>
<dt>rtsp://<%= $ipaddr %>/stream=0</dt>
<dd><%= $t_endpoints_9 %></dd>
<dt>rtsp://<%= $ipaddr %>/stream=1</dt>
<dd><%= $t_endpoints_a %></dd>
</dl>
</div>
</div>
</div>
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_endpoints_b %></div>
<div class="card-body">
<dl>
<dt>http://<%= $ipaddr %>/image.jpg</dt>
<dd><%= $t_endpoints_c %>
<ul class="small">
<li><%= $t_endpoints_d %></li>
<li><%= $t_endpoints_e %></li>
<li><%= $t_endpoints_f %></li>
<li><%= $t_endpoints_g %></li>
</ul>
</dd>
<dt>http://<%= $ipaddr %>/image.heif</dt>
<dd><%= $t_endpoints_h %></dd>
<dt>http://<%= $ipaddr %>/image.yuv420</dt>
<dd><%= $t_endpoints_i %></dd>
<dt>http://<%= $ipaddr %>/image.dng</dt>
<dd><%= $t_endpoints_j %></dd>
</dl>
</div>
</div>
</div>
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_endpoints_k %></div>
<div class="card-body">
<dl>
<dt>http://<%= $ipaddr %>/audio.opus</dt>
<dd><%= $t_endpoints_l %></dd>
<dt>http://<%= $ipaddr %>/audio.pcm</dt>
<dd><%= $t_endpoints_m %></dd>
<dt>http://<%= $ipaddr %>/audio.m4a</dt>
<dd><%= $t_endpoints_n %></dd>
<dt>http://<%= $ipaddr %>/audio.mp3</dt>
<dd><%= $t_endpoints_o %></dd>
<dt>http://<%= $ipaddr %>/audio.alaw</dt>
<dd><%= $t_endpoints_p %></dd>
<dt>http://<%= $ipaddr %>/audio.ulaw</dt>
<dd><%= $t_endpoints_q %></dd>
<dt>http://<%= $ipaddr %>/audio.g711a</dt>
<dd><%= $t_endpoints_r %></dd>
</dl>
</div>
</div>
</div>
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_endpoints_s %></div>
<div class="card-body">
<dl>
<dt>http://<%= $ipaddr %>/night/on</dt>
<dd><%= $t_endpoints_t %></dd>
<dt>http://<%= $ipaddr %>/night/off</dt>
<dd><%= $t_endpoints_u %></dd>
<dt>http://<%= $ipaddr %>/night/toggle</dt>
<dd><%= $t_endpoints_v %></dd>
</dl>
</div>
</div>
</div>
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_endpoints_w %></div>
<div class="card-body">
<dl>
<dt>http://<%= $ipaddr %>/metrics</dt>
<dd><%= $t_endpoints_x %></dd>
</dl>
</div>
</div>
</div>
</div>
<%in p/footer.cgi %>
