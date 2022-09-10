#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="ipeye"
plugin_name="IPEYE"
page_title="IPEYE Cloud"

ipeye_camera_name=$network_hostname
%>
<%in p/header.cgi %>

<p class="alert alert-warning">Attention! This is only a proof of concept for the prospective subsystem of additional services. No real functionality here.</p>

<% if [ "$(yaml-cli -g .ipeye.enabled)" = "true" ]; then %>
  <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
    <div class="col order-2 order-lg-1">
      <h3>Add a feed</h3>
      <form action="<%= $SCRIPT_NAME %>" method="post">
        <% field_text "ipeye_username" "IPEYE cloud username" %>
        <% field_password "ipeye_password" "IPEYE cloud password" %>
        <% field_text "ipeye_camera_name" "Camera name" %>
        <% field_select "ipeye_rtsp_feed" "RTSP feed" "rtsp://${network_address}/stream=0,rtsp://${network_address}/stream=1" %>
        <% button_submit "Add camera to the cloud" %>
      </form>
    </div>
    <div class="col order-1 order-lg-2">
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
      <% field_hidden "mj_ipeye_enabled" "true" %>
      <% button_submit "Enable IPEYE Cloud protocol" "warning" %>
    </form>
  </div>
<% fi %>

<%in p/footer.cgi %>
