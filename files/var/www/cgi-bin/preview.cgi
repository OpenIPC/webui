#!/usr/bin/haserl
content-type: text/html

<% ipaddr=$(yaml-cli -g .network.lan.ipaddr) %>
<%in _header.cgi %>
<h2>Camera preview</h2>

<img src="http://<%= $ipaddr %>/image.jpg" alt="" class="img-fluid border" width="1600" height="900">

<ul class="nav nav-pills justify-content-center">
 <li class="nav-item"><a class="nav-link" href="">🡄</a></li>
 <li class="nav-item"><a class="nav-link" href="">🡆</a></li>
 <li class="nav-item"><a class="nav-link" href="">🡅</a></li>
 <li class="nav-item"><a class="nav-link" href="">🡇</a></li>
 <li class="nav-item"><a class="nav-link" href="">+</a></li>
 <li class="nav-item"><a class="nav-link" href="">-</a></li>
</ul>
<%in _footer.cgi %>
