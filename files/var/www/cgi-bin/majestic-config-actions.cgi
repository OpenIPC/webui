#!/usr/bin/haserl
<% page_title="Majestic Maintenance" %>
<%in _common.cgi %>
<%in _header.cgi %>
<div class="row row-cols-1 row-cols-xl-2 g-4 mb-3">
  <div class="col">
    <div class="card h-100">
      <div class="card-header">Backup</div>
      <div class="card-body">
        <p>Download a copy of the actual <b>majestic.yaml</b> file to backup the changes you have done to the default Majestic configuration.</p>
        <a class="btn btn-primary" href="/cgi-bin/majestic-config-backup.cgi">Download Config</a>
      </div>
    </div>
  </div>

  <div class="col">
    <div class="card h-100">
      <div class="card-header">Restore</div>
      <div class="card-body">
        <form action="/cgi-bin/majestic-config-restore.cgi" method="post" enctype="multipart/form-data">
          <div class="row mb-3">
            <p>Restore your custom Majestic configuration from a backup copy of <b>majestic.yaml</b> file.</p>
            <label class="col-md-3 form-label" for="upfile">Backup file</label>
            <div class="col-md-9">
              <input class="form-control" type="file" name="upfile" placeholder="majestic.yaml">
            </div>
          </div>
          <button type="submit" class="btn btn-danger">Upload Config</button>
        </form>
      </div>
    </div>
  </div>

  <div class="col">
    <div class="card h-100">
      <div class="card-header">Changes</div>
      <div class="card-body">
        <p>Compare your recent configuration of Majestic with the original configuration supplied with the firmware.</p>
        <a class="btn btn-primary" href="/cgi-bin/majestic-config-compare.cgi">Review Changes</a>
      </div>
    </div>
  </div>

  <div class="col">
    <div class="card h-100">
      <div class="card-header">Reset</div>
      <div class="card-body">
        <p>Reset Majestic configuration to its original state, as supplied with the firmware.</p>
        <a class="btn btn-danger" href="/cgi-bin/majestic-config-reset.cgi">Reset Configuration</a>
      </div>
    </div>
  </div>
</div>
<%in _footer.cgi %>
