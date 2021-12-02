#!/usr/bin/haserl
content-type: text/html

<%
# [
# {name: 'hostname', placeholder: 'device-name'},
# {name: 'password', placeholder: 'K0oLHaZk3R!'},
# {name: 'ipaddr', placeholder: '192.168.10.10'},
# {name: 'netmask', placeholder: '255.255.255.0'},
# {name: 'remote', placeholder: 'vtun.net'},
# ]
%>
<%in _header.cgi %>

<div class="cards">
<div>
<form action="/cgi-bin/update.cgi" method="post">
<input type="hidden" name="action" value="update">
<h3>Camera Settings</h3>
<dl>
<dt>Device Name</dt>
<dd><input name="hostname" value="<% hostname -s %>"></dd>
<dt>Interface Password</dt>
<dd><input name="password" value="<% awk -F ':' '/cgi-bin/ {print $3}' /etc/httpd.conf %>"></dd>
<dt>IP Address</dt>
<dd><input name="ipaddr" value="<% yaml-cli -g .network.lan.ipaddr %>" data-real="<% ifconfig eth0 | grep "inet " | tr ':' ' ' | awk '{print $3}' %>"></dd>
<dt>IP Netmask</dt>
<dd><input name="netmask" value="<% yaml-cli -g .network.lan.netmask %>" data-real="<% ifconfig eth0 | grep "inet " | tr ':' ' ' | awk '{print $7}' %>"></dd>
<dt>VTUNd Server</dt>
<dd><input name="remote" value="<% yaml-cli -g .openvpn.vpn1.remote %>" placeholder="vtun.net"></dd>
</dl>
<p><input type="submit" value="Save Settings"></p>
</form>
</div>

<div class="danger">
<form action="/cgi-bin/upload.cgi" method="post" enctype="multipart/form-data">
<input type="hidden" name="action" value="kernel">
<h3>Update kernel</h3>
<dl>
<dt>kernel file</dt>
<dd><input type="file" name="upfile"></dd>
</dl>
<p><input type="submit" value="Upload File"></p>
</form>

<h3>Update rootfs</h3>
<form action="/cgi-bin/upload.cgi" method="post" enctype="multipart/form-data">
<input type="hidden" name="action" value="rootfs">
<dl>
<dt>rootfs file</dt>
<dd><input type="file" name="upfile"></dd>
</dl>
<p><input type="submit" value="Upload File"></p>
</form>

<h3>Reset configuration</h3>
<form action="/cgi-bin/update.cgi" method="post" class="confirm">
<input type="hidden" name="action" value="reset">
<p><input type="submit" value="Reset Configuration"></p>
</form>
</div>
</div>

<%in _footer.cgi %>
