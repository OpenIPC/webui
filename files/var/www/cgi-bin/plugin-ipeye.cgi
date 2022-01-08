#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_system_info
plugin="ipeye"
page_title="IP EYE Cloud"
%>
<%in _header.cgi %>
<div class="alert alert-info">
Attention! This is only a proof of concept for the prospective subsystem of additional services.
No real functionality here.
</div>
<% if [ "$(yaml-cli -g .ipeye.enabled)" != "true" ]; then %>
<div class="alert alert-warning">
  <h4>Cannot proceed because IP EYE support is disabled.</h4>
  <p>In order to add this camera to the cloud you have to enable IP EYE support first.</p>
  <form action="/cgi-bin/majestic-settings-update.cgi" method="post">
  <input type="hidden" name="ipeye-enabled" value="true">
  <input type="hidden" name="go-to" value="<%= $REQUEST_URI %>">
  <button type"submit" class="btn btn-warning">Enable IP EYE support</button>
  </form>
</div>
<% else %>
<div class="row row-cols-1 row-cols-xl-2 g-4 mb-3">
  <div class="col order-sm-2 order-xl-1">
    <div class="card h-100">
      <div class="card-header">Add a feed</div>
      <div class="card-body">
        <form>
          <div class="form-group mb-3">
            <label class="form-label" for="login">IP EYE cloud login</label>
            <input class="form-control" type="text" id="login" name="login">
          </div>
          <div class="form-group mb-3">
            <label class="form-label" for="password">IP EYE cloud password</label>
            <input class="form-control" type="password" id="password" name="password">
          </div>
          <div class="form-group mb-3">
            <label class="form-label" for="password">Camera name</label>
            <input class="form-control" type="text" id="name" name="name" value="<%= $hostname %>">
          </div>
          <div class="form-group mb-3">
            <label class="form-label" for="password">RTSP feed</label>
            <select class="form-select" id="rtsp" name="rtsp">
              <option>rtsp://<%= $ipaddr %>/stream=0</option>
              <option>rtsp://<%= $ipaddr %>/stream=1</option>
            </select>
          </div>
          <button type="submit" class="btn btn-primary">Add camera to the cloud</button>
        </form>
      </div>
    </div>
  </div>
  <div class="col order-sm-1 order-xl-2">
    <p><img src="/img/logo-ipeye.png" alt="IP EYE Logo"></p>
    <p><a href="https://www.ipeye.ru/">www.ipeye.ru</a></p>
    <p>Don't have an account? <a href="https://www.ipeye.ru/">Sign-up here</a></p>
  </div>
</div>
<script>
function handleSubmit(event) {
  event.preventDefault();
  alert('Add registraiton request to API endpoint here.');
  // API v1 doc: http://31.131.248.100/v1/
  // API v2 doc: http://api.ipeye.ru/doc
}
function initIpEyeForm() {
  $('form').addEventListener('submit', handleSubmit);
}
window.addEventListener('load', initIpEyeForm);
</script>
<% fi %>
<%in _footer.cgi %>
