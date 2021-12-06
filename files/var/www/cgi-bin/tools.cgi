#!/usr/bin/haserl
content-type: text/html

<%in _header.cgi %>
<% interfaces=$(/sbin/ifconfig | grep '^\w' | awk {'print $1'}) %>
<h2>Monitoring Tools</h2>

<div class="row row-cols-1 row-cols-xl-2 g-4 mb-4">
<div class="col">
<div class="card h-100 mb-3">
<h5 class="card-header">Ping Quality</h5>
<div class="card-body">
<form action="/cgi-bin/tools-do.cgi" method="post">
<div class="row mb-3">
<div class="col-md-6">
<label for="action">Action</label>
</div>
<div class="col-md-6">
<select name="action" id="action">
<option></option>
<% for i in ping trace; do echo -n "<option>${i}</option>"; done %>
</select>
</div>
</div>
<div class="row mb-3">
<div class="col-md-6">
<label for="target">Target FQDN or IP address</label>
</div>
<div class="col-md-6">
<input type="text" name="target" id="target" pattern="^[a-zA-Z0-9-_.]+$" value="4.2.2.1" placeholder="FQDN or IP address" required>
</div>
</div>
<div class="row mb-3">
<div class="col-md-6">
<label for="iface">Use network interface</label>
</div>
<div class="col-md-6">
<select name="iface" id="iface">
<option>auto</option>
<% for i in $interfaces; do echo -n "<option>${i}</option>"; done %>
</select>
</div>
</div>
<p class="mb-0">
<input type="submit" value="Run" class="btn btn-primary">
</p>
</form>
</div>
</div>
</div>
</div>

<%in _footer.cgi %>
