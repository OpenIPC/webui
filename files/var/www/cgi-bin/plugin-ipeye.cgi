#!/usr/bin/haserl
<%in _common.cgi %>
<%
plugin="ipeye"
page_title="IPEYE Cloud"
hostname=$(hostname -s)
ipaddr=$(printenv | grep HTTP_HOST | cut -d= -f2 | cut -d: -f1)
%>
<%in _header.cgi %>
<div class="alert alert-warning">Attention! This is only a proof of concept for the prospective subsystem of additional services. No real functionality here.</div>

<div class="row row-cols-1 row-cols-xl-2 g-4 mb-3">
  <div class="col order-sm-2 order-xl-1">
    <div class="card h-100">
      <div class="card-header">Add a feed</div>
      <div class="card-body">
        <form>
          <div class="form-group mb-3">
            <label class="form-label" for="login">IPEYE cloud login</label>
            <input class="form-control" type="text" id="login" name="login">
          </div>
          <div class="form-group mb-3">
            <label class="form-label" for="password">IPEYE cloud password</label>
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
    <p><img src="/img/logo-ipeye.png" alt="IPEYE Logo"></p>
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
<%in _footer.cgi %>
