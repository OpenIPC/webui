#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="Reset things" %>
<%in p/header.cgi %>

<div class="row g-4">
  <div class="col">
    <div class="alert alert-danger">
      <h4>Reboot camera</h4>
      <p>Reboot camera to apply new settings. That will also delete all data on partitions mounted into system memory, like /tmp and such.</p>
      <p class="mb-0"><a class="btn btn-danger" href="reboot.cgi">Reboot camera</a></p>
    </div>

    <%in p/reset-firmware.cgi %>

    <div class="alert alert-danger">
      <h4>Reset Majestic settings</h4>
      <p>Revert Majestic configuration to default setings. All changes will be lost! You might want to back up your recent configuration first.</p>
      <p class="d-flex gap-2 mb-0">
        <form action="majestic-config-actions.cgi" method="post">
          <input type="hidden" name="action" value="backup">
          <input type="submit" class="btn btn-primary" value="Backup settings">
        </form>

        <form action="majestic-config-actions.cgi" method="post">
          <input type="hidden" name="action" value="reset">
          <input type="submit" class="btn btn-danger" value="Reset settings" title="Restore original configuration">
        </form>
      </p>
    </div>
  </div>
</div>

<%in p/footer.cgi %>
