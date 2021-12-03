#!/usr/bin/haserl
content-type: text/html

<%in _header.cgi %>
<h2>Global Settings</h2>
<div class="row row-cols-1 row-cols-md-2 g-4 mb-4">
<div class="col">
<div class="card h-100 mb-3">
<h5 class="card-header">Camera Settings</h5>
<div class="card-body">
<form action="/cgi-bin/update.cgi" method="post">
<input type="hidden" name="action" value="update">
<div class="row mb-3">
<div class="col-md-5"><label for="hostname" class="form-label">Device Name</label></div>
<div class="col-md-7"><input type="text" class="form-control" name="hostname" id="hostname" value="<% hostname -s %>" placeholder="device-name"></div>
</div>
<div class="row mb-3">
<div class="col-md-5"><label for="password" class="form-label">Interface Password</label></div>
<div class="col-md-7"><input type="password" class="form-control" name="password" id="password" value="<% awk -F ':' '/cgi-bin/ {print $3}' /etc/httpd.conf %>" placeholder="K3wLHaZk3R!"></div>
</div>
<div class="row mb-3">
<div class="col-md-5"><label for="ipaddr" class="form-label">IP Address</label></div>
<div class="col-md-7"><input type="text" class="form-control" name="ipaddr" id="ipaddr" value="<% yaml-cli -g .network.lan.ipaddr %>" data-real="<% ifconfig eth0 | grep "inet " | tr ':' ' ' | awk '{print $3}' %>" placeholder="192.168.10.10"></div>
</div>
<div class="row mb-3">
<div class="col-md-5"><label for="netmask" class="form-label">IP Netmask</label></div>
<div class="col-md-7"><input type="text" class="form-control" name="netmask" id="netmask" value="<% yaml-cli -g .network.lan.netmask %>" data-real="<% ifconfig eth0 | grep "inet " | tr ':' ' ' | awk '{print $7}' %>" placeholder="255.255.255.0"></div>
</div>
<div class="row mb-3">
<div class="col-md-5"><label for="remote" class="form-label">VTUNd Server</label></div>
<div class="col-md-7"><input type="text" class="form-control" name="remote" id="remote" value="<% yaml-cli -g .openvpn.vpn1.remote %>" placeholder="vtun.net"></div>
</div>
<div class="row">
<div class="col"><input type="submit" class="btn btn-primary" value="Save Settings"></div>
</div>
</form>
</div>
</div>
</div>

<div class="col">
<div class="alert alert-danger mb-0">
<a class="btn btn-danger float-end" href="/cgi-bin/reboot.cgi">Reboot</a>
<h5 class="mb-4">Attention: Destructive Actions!</h5>

<div class="card mb-3 danger">
<h5 class="card-header">Update kernel</h5>
<div class="card-body">
<form action="/cgi-bin/upload.cgi" method="post" enctype="multipart/form-data">
<input type="hidden" name="action" value="kernel">
<div class="row">
<div class="col-12 mb-3"><label for="upfile">kernel file</label></div>
<div class="col-12 mb-3"><input type="file" name="upfile"></div>
</div>
<p><input type="submit" class="btn btn-danger" value="Upload File"></p>
</form></div></div>

<div class="card mb-3 danger">
<h5 class="card-header">Update rootfs</h5>
<div class="card-body">
<form action="/cgi-bin/upload.cgi" method="post" enctype="multipart/form-data">
<input type="hidden" name="action" value="rootfs">
<div class="row">
<div class="col-12 mb-3"><label for="upfile">rootfs file</div>
<div class="col-12 mb-3"><input type="file" name="upfile"></div>
</div>
<p><input type="submit" class="btn btn-danger" value="Upload File"></p>
</form></div></div>

<div class="card mb-0 danger">
<h5 class="card-header">Reset configuration</h5>
<div class="card-body">
<form action="/cgi-bin/reset.cgi" method="post">
<input type="hidden" name="action" value="reset">
<p><input type="submit" class="btn btn-danger" value="Reset Configuration"></p>
</form></div></div>

</div>
</div>
</div>

<%in _footer.cgi %>
