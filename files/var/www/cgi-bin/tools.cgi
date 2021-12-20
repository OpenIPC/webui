#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="Monitoring Tools"
interfaces=$(/sbin/ifconfig | grep '^\w' | awk {'print $1'})
%>
<%in _header.cgi %>
<div class="row row-cols-1 row-cols-xl-2 g-4 mb-4">
  <div class="col">
    <div class="card h-100 mb-3">
      <h5 class="card-header">Ping Quality</h5>
      <div class="card-body">
        <form action="/cgi-bin/tools-do.cgi" method="post">
          <div class="row mb-2">
            <label class="form-label col-md-6" for="action">Action</label>
            <div class="col-md-6">
              <select class="form-select" name="action" id="action">
                <% for i in ping trace; do echo -n "<option>${i}</option>"; done %>
              </select>
            </div>
          </div>
          <div class="row mb-2">
            <label class="col-md-6 form-label" for="target">Target FQDN or IP address</label>
            <div class="col-md-6">
              <input class="form-control pat-host-ip" type="text" name="target" id="target" value="4.2.2.1" placeholder="FQDN or IP address" required>
            </div>
          </div>
          <div class="row mb-2">
            <label class="col-md-6 form-label" for="iface">Use network interface</label>
            <div class="col-md-6">
              <select class="form-select" name="iface" id="iface">
                <option>auto</option>
                <% for i in $interfaces; do echo -n "<option>${i}</option>"; done %>
              </select>
            </div>
          </div>
          <button type="submit" class="btn btn-primary">Run</button>
        </form>
      </div>
    </div>
  </div>
</div>

<%in _footer.cgi %>
