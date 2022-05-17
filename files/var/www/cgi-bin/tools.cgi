#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_system_info
page_title="$tPageTitleTools"
%>
<%in _header.cgi %>
<div class="row row-cols-1 row-cols-xl-2 g-4 mb-4">
<div class="col">
<div class="card h-100 mb-3">
<h5 class="card-header"><%= $tHeaderPing %></h5>
<div class="card-body">
<form action="/cgi-bin/tools-do.cgi" method="post">
<div class="row mb-2">
<label class="form-label col-md-6" for="action"><%= $tLabelPingAction %></label>
<div class="col-md-6">
<select class="form-select" name="action" id="action">
<% for i in ping trace; do echo -n "<option>${i}</option>"; done %>
</select>
</div>
</div>
<div class="row mb-2">
<label class="col-md-6 form-label" for="target"><%= $tLabelPingTarget %></label>
<div class="col-md-6">
<input class="form-control pat-host-ip" type="text" name="target" id="target" value="4.2.2.1" placeholder="FQDN or IP address" required>
</div>
</div>
<div class="row mb-2">
<label class="col-md-6 form-label" for="iface"><%= $tLabelPingInterface %></label>
<div class="col-md-6">
<select class="form-select" name="iface" id="iface">
<option>auto</option>
<% for i in $interfaces; do echo -n "<option>${i}</option>"; done %>
</select>
</div>
</div>
<div class="row mb-2">
<label class="col-md-6 form-label" for="size"><%= $tLabelPingPacketSize %></label>
<div class="col-md-6">
<div class="input-group">
<span class="input-group-text">
<label><input type="checkbox" class="form-check-input auto-value" data-for="size" data-value=""> default</label>
</span>
<input class="form-control" type="number" min="56" max="1500" step="1" name="size" id="size" value="56">
</div>
</div>
</div>
<div class="row mb-2">
<label class="col-md-6 form-label" for="duration"><%= $tLabelPingDuration %></label>
<div class="col-md-6">
<input class="form-control" type="number" min="1" max="30" step="1" name="duration" id="duration" value="5">
</div>
</div>
<button type="submit" class="btn btn-primary"><%= $tButtonRun %></button>
</form>
</div>
</div>
</div>
</div>
<%in _footer.cgi %>
