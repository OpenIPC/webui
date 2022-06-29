#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="ipeye"
plugin_name="IPEYE"
page_title="IPEYE Cloud"
%>
<%in p/header.cgi %>

<p class="alert alert-warning">Attention! This is only a proof of concept for the prospective subsystem of additional services. No real functionality here.</p>

<% if [ "$(yaml-cli -g .ipeye.enabled)" = "true" ]; then %>
  <div class="row row-cols-1 row-cols-lg-2 row-cols-xxl-3 g-4">
    <div class="col order-2 order-xl-1">
      <h3>Add a feed</h3>
      <form action="<%= $SCRIPT_NAME %>" method="post">
<%
tL_ipeye_camera_name="Camera name"
tL_ipeye_login="IPEYE cloud login"
tL_ipeye_password="IPEYE cloud password"
tL_ipeye_rtsp_feed="RTSP feed"

ipeye_camera_name="$hostname"
field_text "ipeye_login"
field_text "ipeye_password"
field_text "ipeye_password"
field_text "ipeye_camera_name"
field_select "ipeye_rtsp_feed"
button_submit "Add camera to the cloud"
%>
      </form>
    </div>
    <div class="col order-1 order-xl-2">
      <p><img src="/a/logo-ipeye.webp" alt="Image: IPEYE logo" title="IPEYE Logo"></p>
      <p><a href="https://www.ipeye.ru/" target="_blank">www.ipeye.ru</a></p>
      <p>Don't have an account? <a href="https://www.ipeye.ru/" target="_blank">Sign-up here</a></p>
    </div>
  </div>

  <script>
  function handleSubmit(event) {
    event.preventDefault();
    alert("Add registraiton request to API endpoint here.");
    // API v1 doc: http://31.131.248.100/v1/
    // API v2 doc: http://api.ipeye.ru/doc
  }
  function initIpEyeForm() { $("form").addEventListener("submit", handleSubmit); }
  window.addEventListener("load", initIpEyeForm);
  </script>
<% else %>
  <div class="alert alert-danger">
    <h4>Cannot proceed because IPEYE support is disabled.</h4>
    <p>In order to add this camera to the cloud you have to enable IPEYE support first.</p>
    <form action="majestic-settings.cgi" method="post">
      <input type="hidden" name="mj_ipeye_enabled" id="mj_ipeye_enabled" value="true" class="form-control">
      <p class="mt-2"><input type="submit" class="btn btn-warning" value="Enable IPEYE Cloud protocol"></p>
    </form>
  </div>
<% fi %>

<%in p/footer.cgi %>
