#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="Reset things" %>
<%in p/header.cgi %>

<div class="row row-cols-md-3 g-4 mb-4">
  <div class="col">
    <div class="alert alert-danger">
      <h4>Reboot camera</h4>
      <p>Reboot camera to apply new settings. That will also delete all data on partitions mounted into system memory, e.g. /tmp.</p>
      <% button_reboot %>
    </div>
  </div>
  <div class="col">
    <%in p/reset-firmware.cgi %>
  </div>
  <div class="col">
    <div class="alert alert-danger">
      <h4>Reset Majestic settings</h4>
      <p>Revert Majestic configuration file <code>/etc/majestic.yaml</code> to its pristine state. All changes will be lost!
       You might want to <a href="majestic-config-actions.cgi">back up recent configuration</a> before you reset.</p>
      <% button_mj_reset %>
    </div>
  </div>
</div>

<%in p/footer.cgi %>
