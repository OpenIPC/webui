#!/usr/bin/haserl
<%in _common.cgi %>
<% page_title="Firmware Updates"
fw_version=$(cat /etc/os-release | grep "GITHUB_VERSION" | cut -d= -f2 | tr -d /\"/ 2>&1)
mj_version=$(majestic -v)
mj_filesize=$(ls -s /usr/bin/majestic | xargs | cut -d " " -f 1)
majestic_diff=$(diff /rom/etc/majestic.yaml /etc/majestic.yaml)
ui_version=$(cat /var/www/.version)
%>
<%in _header.cgi %>
<div class="alert alert-danger">
  <b>Attention: Destructive Actions!</b>
  <p class="mb-0">Make sure you know what you are doing.</p>
</div>

<div class="row row-cols-1 row-cols-md-2 g-4 mb-4">

  <div class="col">
    <div class="card mb-3">
      <div class="card-header">Firmware</div>
      <div class="card-body">
        <dl class="row">
          <dt class="col-6">Installed</dt>
          <dd class="col-6 text-end"><%= $fw_version %></dd>
          <dt class="col-6">Stable channel</dt>
          <dd class="col-6 text-end" id="firmware-master-ver"></dd>
        </dl>
        <form action="/cgi-bin/firmware-update.cgi" method="post">
          <div class="row mb-3">
            <div class="col-md-10 offset-md-2">
              <input class="form-check-input" type="checkbox" name="kernel" id="kernel" value="true" checked>
              <label class="form-check-label" for="kernel">Upgrade kernel.</label>
            </div>
            <div class="col-md-10 offset-md-2">
              <input class="form-check-input" type="checkbox" name="rootfs" id="rootfs" value="true" checked>
              <label class="form-check-label" for="rootfs">Upgrade rootfs.</label>
            </div>
            <div class="col-md-10 offset-md-2">
              <input class="form-check-input" type="checkbox" name="reset" id="reset" value="true">
              <label class="form-check-label" for="reset">Reset settings after upgrade.</label>
            </div>
            <div class="col-md-10 offset-md-2">
              <input class="form-check-input" type="checkbox" name="noreboot" id="noreboot" value="true">
              <label class="form-check-label" for="noreboot">Do not reboot after upgrade.</label>
            </div>
            <div class="col-md-10 offset-md-2">
              <input class="form-check-input" type="checkbox" name="debug" id="debug-fw" value="true">
              <label class="form-check-label" for="debug-fw">Show debugging information.</label>
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
        <dl class="row">
          <dt class="col-6">Installed</dt>
          <dd class="col-6 text-end"><%= $ui_version %></dd>
          <dt class="col-6">Stable channel</dt>
          <dd class="col-6 text-end" id="microbe-web-master-ver"></dd>
          <dt class="col-6">Unstable channel</dt>
          <dd class="col-6 text-end" id="microbe-web-dev-ver"></dd>
        </dl>
        <form action="/cgi-bin/web-ui-update.cgi" method="post">
          <div class="row mb-1">
            <label class="col-md-2 form-label" for="version">Branch</label>
            <div class="col-md-10">
              <select class="form-select" name="version" id="version">
                <option value="master">stable</option>
                <option value="dev">development</option>
              </select>
            </div>
          </div>
          <div class="row mb-3">
            <div class="col-md-10 offset-md-2">
              <input class="form-check-input" type="checkbox" name="enforce" id="enforce" value="true">
              <label class="form-check-label" for="enforce">Disable version checking.</label>
            </div>
            <div class="col-md-10 offset-md-2">
              <input class="form-check-input" type="checkbox" name="debug" id="debug-ui" value="true">
              <label class="form-check-label" for="debug-ui">Show debugging information.</label>
            </div>
          </div>
          <button type="submit" class="btn btn-danger">Update from GitHub</button>
        </form>
      </div>
    </div>

    <div class="card mb-3">
      <div class="card-header">Majestic</div>
      <div class="card-body">
        <form action="/cgi-bin/majestic-github.cgi" method="post">
          <p><b>Installed ver. <%= $mj_version %></b> <span id="mj-ver-master"></span></p>
          <dl>
          <% if [ -f /overlay/root/usr/bin/majestic ]; then %>
            <dd>Majestic is installed in the overlay. (<%= $mj_filesize %> KB)</dd>
          <% else %>
            <dd>Bundled version of Majestic is used. (<%= $mj_filesize %> KB)</dd>
          <% fi %>
          <% if [ -z "$majestic_diff" ]; then %>
            <dd>Majestic uses the original configuration.
              <a href="/cgi-bin/majestic-settings-general.cgi">Change settings.</a></dd>
          <% else %>
            <dd>Majestic uses custom configuration.
              <a href="/cgi-bin/majestic-config-compare.cgi">See changes.</a></dd>
          <% fi %>
          </dl>
          <div class="row mb-3">
            <div class="col-md-10 offset-md-2">
              <input class="form-check-input" type="checkbox" name="debug" id="debug-mj" value="true">
              <label class="form-check-label" for="debug-mj">Show debugging information.</label>
            </div>
          </div>
          <% if [ ! -z "$majestic_diff" ]; then %>
            <a class="btn btn-danger float-end" href="/cgi-bin/majestic-config-reset.cgi"
                title="Restore original configuration">Reset</a>
          <% fi %>
          <button class="btn btn-danger">Update from GitHub</button>
        </form>
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

<script>
  function checkUpdates() {
    queryBranch('firmware', 'master');
    queryBranch('microbe-web', 'master');
    queryBranch('microbe-web', 'dev');
  }

  function queryBranch(repo, branch) {
    var oReq = new XMLHttpRequest();
    oReq.addEventListener("load", function(){
      const d = JSON.parse(this.response);
      const sha_short = d.commit.sha.slice(0,7);
      const date = d.commit.commit.author.date.slice(0,10);
      const link = document.createElement('a');
      link.href = 'https://github.com/OpenIPC/' + repo + '/commits/' + branch;
      link.target = '_blank';
      link.textContent = branch + '+' + sha_short + ', ' + date;
      const el = $('#' + repo + '-' + branch + '-ver').appendChild(link);
    });
    oReq.open("GET", 'https://api.github.com/repos/OpenIPC/' + repo + '/branches/' + branch);
    oReq.send();
  }

  window.addEventListener('load', checkUpdates);
</script>

<%in _footer.cgi %>
