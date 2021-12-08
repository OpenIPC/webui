#!/usr/bin/haserl
<%
ui_date=$(ls -d --full-time /var/www/.etag | xargs | cut -d " " -f 6,7)
ui_version=$(date --date="$ui_date" +"%s")

fw_version=$(cat /etc/os-release | grep "OPENIPC_VERSION" | cut -d= -f2 2>&1)

majestic_diff=$(diff /rom/etc/majestic.yaml /etc/majestic.yaml)
%>
<%in _header.cgi %>
<h2>Firmware Updates</h2>

<div class="alert alert-danger">
  <b>Attention: Destructive Actions!</b>
  <p class="mb-0">Make sure you know what you are doing.</p>
</div>

<div class="row row-cols-1 row-cols-md-2 g-4 mb-4">

  <div class="col">
    <div class="card mb-3">
      <div class="card-header">Firmware</div>
      <div class="card-body">
        <p><b>Installed ver.<%= $fw_version %></b></p>
        <form action="/cgi-bin/firmware-update.cgi" method="post">
          <div class="row mb-3">
            <div class="col-md-10 offset-md-2">
              <input class="form-check-input" type="checkbox" name="reset" id="reset" value="true">
              <label class="form-check-label" for="reset">Reset settings after upgrade.</label>
            </div>
          </div>
          <a class="btn btn-danger float-end" title="Wipe overlay partition">Reset</a>
          <button type="submit" class="btn btn-danger">Update from GitHub</button>
        </form>
      </div>
    </div>

    <div class="card mb-3">
      <div class="card-header">Web UI</div>
      <div class="card-body">
        <p><b>Installed ver.<%= $ui_version %></b></p>
        <form action="/cgi-bin/web-ui-update.cgi" method="post">
          <div class="row mb-1">
            <label class="col-md-2 form-label" for="version">Branch</label>
            <div class="col-md-10">
              <select class="form-select" name="version" id="version">
                <option>stable</option>
                <option>development</option>
              </select>
            </div>
          </div>
          <div class="row mb-3">
            <div class="col-md-10 offset-md-2">
              <input class="form-check-input" type="checkbox" name="enforce" id="enforce" value="true">
              <label class="form-check-label" for="enforce">disable version checking</label>
            </div>
          </div>
          <button type="submit" class="btn btn-danger">Update from GitHub</button>
        </form>
      </div>
    </div>

    <div class="card mb-3">
      <div class="card-header">Majestic</div>
      <div class="card-body">
        <% if [ -z "$majestic_diff" ]; then %>
          <p><b>Majestic uses the original configuration.</b>
            <a href="/cgi-bin/majestic.cgi">Change settings.</a></p>
        <% else %>
          <p><b>Majestic uses custom configuration.</b>
            <a href="/cgi-bin/majestic-diff.cgi">See changes.</a></p>
        <% fi %>
        <p class="mb-0">
          <% if [ ! -z "$majestic_diff" ]; then %>
            <a class="btn btn-danger float-end" href="/cgi-bin/majestic-reset.cgi"
              title="Restore original configuration">Reset</a>
          <% fi %>
          <a class="btn btn-danger" href="/cgi-bin/github-majestic.cgi">Update from GitHub</a>
        </p>
      </div>
    </div>

  </div>
  <div class="col">

    <div class="card mb-3">
      <div class="card-header">Camera</div>
      <div class="card-body">
        <a class="btn btn-warning" href="/cgi-bin/reboot.cgi">Reboot camera</a>
      </div>
    </div>

    <div class="card mb-3">
      <div class="card-header">Upload kernel</div>
      <div class="card-body">
        <form action="/cgi-bin/firmware-upload-kernel.cgi" method="post" enctype="multipart/form-data">
          <div class="row mb-3">
            <label class="col-md-3 form-label" for="upfile">kernel file</label>
            <div class="col-md-9">
              <input class="form-control" type="file" name="upfile">
            </div>
          </div>
          <button type="submit" class="btn btn-danger">Upload file</button>
        </form>
      </div>
    </div>

    <div class="card mb-3">
      <div class="card-header">Upload rootfs</div>
      <div class="card-body">
        <form action="/cgi-bin/firmware-upload-rootfs.cgi" method="post" enctype="multipart/form-data">
          <div class="row mb-3">
            <label class="col-md-3 form-label" for="upfile">rootfs file</label>
            <div class="col-md-9">
              <input class="form-control" type="file" name="upfile">
            </div>
          </div>
          <button type="submit" class="btn btn-danger">Upload file</button>
        </form>
      </div>
    </div>
  </div>
</div>

<%in _footer.cgi %>
