#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_soc
get_firmware_info
page_title="Firmware Updates"
mj_bin_file="/usr/bin/majestic"
mj_version=$(${mj_bin_file} -v)
ui_version=$(cat /var/www/.version)
mj_meta_url="http://openipc.s3-eu-west-1.amazonaws.com/majestic.${soc}.${fw_variant}.master.tar.meta"
mj_config_diff=$(diff /rom/etc/majestic.yaml /etc/majestic.yaml)
[ -f /overlay/root/${mj_bin_file} ] && mj_filesize_old=$(ls -s ${mj_bin_file} | xargs | cut -d" " -f1) || mj_filesize_old=0
mj_filesize_new=$(curl -vv ${mj_meta_url})
mj_filesize_new=$(echo $mj_filesize_new / 1024 | bc)
free_space=$(df | grep /overlay | xargs | cut -d" " -f4)
available_space=$(( $free_space + $mj_filesize_old - 1 ))
%>
<%in _header.cgi %>
<div class="alert alert-danger">
  <b>Attention: Destructive Actions!</b>
  <p class="mb-0">Make sure you know what you are doing.</p>
</div>
<div class="row row-cols-1 row-cols-md-2 row-cols-xl-3 g-4 mb-4">
  <div class="col">
    <div class="card h-100">
      <div class="card-header">Firmware</div>
      <div class="card-body">
        <dl class="row">
          <dt class="col-4">Installed</dt>
          <dd class="col-8 text-end"><%= $fw_version %></dd>
          <dt class="col-4">Latest</dt>
          <dd class="col-8 text-end" id="firmware-master-ver"></dd>
        </dl>
        <div class="alert alert-light">
          <p><b>Install update.</b></p>
          <form action="/cgi-bin/firmware-update.cgi" method="post">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" name="kernel" id="kernel" value="true" checked>
              <label class="form-check-label" for="kernel">Upgrade kernel.</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" name="rootfs" id="rootfs" value="true" checked>
              <label class="form-check-label" for="rootfs">Upgrade rootfs.</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" name="reset" id="reset" value="true">
              <label class="form-check-label" for="reset">Reset firmware.</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" name="noreboot" id="noreboot" value="true">
              <label class="form-check-label" for="noreboot">Do not reboot after upgrade.</label>
            </div>
            <p class="mt-3 mb-0"><button type="submit" class="btn btn-warning">Install update</button></p>
          </form>
        </div>
        <div class="alert alert-danger mb-0">
          <p><b>Reset firmware.</b></p>
          <p>Revert firmware to its original state by wiping out content of the overlay partition. All custom settings will be lost!</p>
          <p class="mb-0"><a class="btn btn-danger" href="/cgi-bin/firmware-reset.cgi"
            title="Wipe overlay partition">Reset firmware</a></p>
        </div>
      </div>
    </div>
  </div>
  <div class="col">
    <div class="card h-100">
      <div class="card-header">Web UI</div>
      <div class="card-body">
        <dl class="row">
          <dt class="col-4">Installed</dt>
          <dd class="col-8 text-end"><%= $ui_version %></dd>
          <dt class="col-4">Stable</dt>
          <dd class="col-8 text-end" id="microbe-web-master-ver"></dd>
          <dt class="col-4">Unstable</dt>
          <dd class="col-8 text-end" id="microbe-web-dev-ver"></dd>
        </dl>
        <div class="alert alert-light">
          <p><b>Install update.</b></p>
          <form action="/cgi-bin/web-ui-update.cgi" method="post">
            <label class="form-label" for="version">Update from the following branch:</label>
            <select class="form-select mb-2" name="version" id="version">
              <option value="master">stable</option>
              <option value="dev">development</option>
            </select>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" name="enforce" id="enforce" value="true">
              <label class="form-check-label" for="enforce">Install even if matches the existing version.</label>
            </div>
            <p class="mt-3 mb-0"><button type="submit" class="btn btn-warning">Install update</button></p>
          </form>
        </div>
      </div>
    </div>
  </div>
  <div class="col">
    <div class="card h-100">
      <div class="card-header">Majestic</div>
      <div class="card-body">
        <dl class="row">
          <dt class="col-4">Installed</dt>
          <dd class="col-8 text-end"><%= $mj_version %></dd>
          <dt class="col-4">Latest</dt>
          <dd class="col-8 text-end" id="mj-ver-master"></dd>
        </dl>
        <div class="alert alert-light">
        <% if [ -f /overlay/root/usr/bin/majestic ]; then %>
          <p><b>Majestic is installed in the overlay.</b> (<%= $mj_filesize_old %> KB)</p>
        <% else %>
          <p><b>Bundled version of Majestic is used.</b></p>
        <% fi %>
        <% if [ "$mj_filesize_new" -le "$available_space" ]; then %>
          <form action="/cgi-bin/majestic-github.cgi" method="post">
            <p><button class="btn btn-warning">Install update</button></p>
          </form>
        <% else %>
          <div class="alert alert-warning">Not enough space to update Majestic.<br>
            Required <%= $mj_filesize_new %> KB, available <%= $available_space %> KB.</div>
        <% fi %>
        </div>
        <div class="alert alert-light mb-0">
        <% if [ -z "$mj_config_diff" ]; then %>
          <p><b>Majestic uses the original configuration.</b></p>
          <p class="mb-0"><a href="/cgi-bin/majestic-settings-general.cgi">Make changes.</a></p>
        <% else %>
          <p><b>Majestic uses custom configuration.</b></p>
          <p><a href="/cgi-bin/majestic-config-compare.cgi">See changes.</a></p>
          <div class="alert alert-danger mb-0">
            <p><b>Reset Majestic settings.</b></p>
            <p>Revert Majestic configuration to default setings. All changes will be lost! You might want to <a href="/cgi-bin/majestic-config-backup.cgi">backup your recent configuration</a> first.</p>
            <p class="mb-0"><a class="btn btn-danger" href="/cgi-bin/majestic-config-reset.cgi" title="Restore original configuration">Reset settings</a></p>
          </div>
        <% fi %>
        </div>
      </div>
    </div>
  </div>
  <div class="col">
    <div class="card h-100">
      <div class="card-header">Camera</div>
      <div class="card-body">
        <a class="btn btn-warning" href="/cgi-bin/reboot.cgi">Reboot camera</a>
      </div>
    </div>
  </div>
  <div class="col">
    <div class="card h-100">
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
  </div>
  <div class="col">
    <div class="card h-100">
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
    //queryRelease();
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
  function queryRelease() {
    var oReq = new XMLHttpRequest();
    oReq.addEventListener("load", function(){
      const d = JSON.parse(this.response);
      const asset = d[0].assets.find(a => a['name'] === 'openipc.<%= $soc %>-br.tgz');
      const date = asset.created_at.slice(0,10);
      const sha_short = asset.target_commitish.slice(0,7);
      const link = document.createElement('a');
      link.href = 'https://github.com/OpenIPC/firmware/commits/master';
      link.target = '_blank';
      link.textContent = 'master+' + sha_short + ', ' + date;
      const el = $('#firmware-master-ver').appendChild(link);
    });
    oReq.open("GET", 'https://api.github.com/repos/OpenIPC/firmware/releases');
    oReq.send();
  }
  window.addEventListener('load', checkUpdates);
</script>
<%in _footer.cgi %>
