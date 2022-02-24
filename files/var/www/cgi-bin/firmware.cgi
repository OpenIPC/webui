#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_hardware_info
get_firmware_info
get_software_info

page_title="$tPageTitleFirmware"
mj_meta_url="http://openipc.s3-eu-west-1.amazonaws.com/majestic.${soc_family}.${fw_variant}.master.tar.meta"
mj_config_diff=$(diff /rom/etc/majestic.yaml /etc/majestic.yaml)
[ -f /overlay/root/${mj_bin_file} ] && mj_filesize_old=$(ls -s ${mj_bin_file} | xargs | cut -d" " -f1) || mj_filesize_old=0
mj_filesize_new=$(curl -s ${mj_meta_url})
mj_filesize_new=$(echo $mj_filesize_new / 1024 | bc)
free_space=$(df | grep /overlay | xargs | cut -d" " -f4)
available_space=$(( $free_space + $mj_filesize_old - 1 ))
%>
<%in _header.cgi %>
<div class="alert alert-danger">
  <b><%= $tMsgDestructiveActions %></b>
  <p class="mb-0"><%= $tMsgKnowWhatYouDo %></p>
</div>
<div class="row row-cols-1 row-cols-md-2 row-cols-xl-3 g-4 mb-4">
  <div class="col">
    <div class="card h-100">
      <div class="card-header"><%= $tHeaderFirmware %></div>
      <div class="card-body">
        <dl class="row">
          <dt class="col-4"><%= $tInstalled %></dt>
          <dd class="col-8 text-end"><%= $fw_version %></dd>
          <dt class="col-4"><%= $tLatest %></dt>
          <dd class="col-8 text-end" id="firmware-master-ver"></dd>
        </dl>
        <div class="alert alert-light">
          <p><b><%= $tInstallUpdate %>.</b></p>
          <form action="/cgi-bin/firmware-update.cgi" method="post">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" name="kernel" id="kernel" value="true" checked>
              <label class="form-check-label" for="kernel"><%= $tLabelUpgradeKernel %></label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" name="rootfs" id="rootfs" value="true" checked>
              <label class="form-check-label" for="rootfs"><%= $tLabelUpgradeRootfs %></label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" name="reset" id="reset" value="true">
              <label class="form-check-label" for="reset"><%= $tLabelResetFirmware %></label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" name="noreboot" id="noreboot" value="true">
              <label class="form-check-label" for="noreboot"><%= $tLabelDoNotReboot %></label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" name="enforce" id="enforce" value="true">
              <label class="form-check-label" for="enforce"><%= $tOverwriteSameVersion %></label>
            </div>
            <p class="mt-3 mb-0"><button type="submit" class="btn btn-warning"><%= $tButtonInstallUpdate %></button></p>
          </form>
        </div>
        <div class="alert alert-danger mb-0">
          <p><b><%= $tResetFirmware %></b></p>
          <p><%= $tResetFirmwareInfo %></p>
          <p class="mb-0"><a class="btn btn-danger" href="/cgi-bin/firmware-reset.cgi" title="<%= $tResetFirmwareTitle %>"><%= $tButtonResetFirmware %></a></p>
        </div>
      </div>
    </div>
  </div>
  <div class="col">
    <div class="card h-100">
      <div class="card-header"><%= $tHeaderWebui %></div>
      <div class="card-body">
        <dl class="row">
          <dt class="col-4"><%= $tInstalled %></dt>
          <dd class="col-8 text-end"><%= $ui_version %></dd>
          <dt class="col-4"><%= $tStable %></dt>
          <dd class="col-8 text-end" id="microbe-web-master-ver"></dd>
          <dt class="col-4"><%= $tUnstable %></dt>
          <dd class="col-8 text-end" id="microbe-web-dev-ver"></dd>
        </dl>
        <div class="alert alert-light">
          <p><b><%= $tInstallUpdate %>.</b></p>
          <form action="/cgi-bin/webui-update.cgi" method="post">
            <label class="form-label" for="version"><%= $tUpdateFromBranch %>:</label>
            <select class="form-select mb-2" name="version" id="version">
              <option value="master">stable</option>
              <option value="dev">development</option>
            </select>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" name="enforce" id="enforce" value="true">
              <label class="form-check-label" for="enforce"><%= $tOverwriteSameVersion %></label>
            </div>
            <p class="mt-3 mb-0"><button type="submit" class="btn btn-warning"><%= $tButtonInstallUpdate %></button></p>
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
          <dt class="col-4"><%= $tInstalled %></dt>
          <dd class="col-8 text-end"><%= $mj_version %></dd>
          <dt class="col-4"><%= $tLatest %></dt>
          <dd class="col-8 text-end" id="mj-ver-master"></dd>
        </dl>
        <div class="alert alert-light">
        <% if [ -f /overlay/root/usr/bin/majestic ]; then %>
          <p><b><%= $tMjInOverlay %></b> (<%= $mj_filesize_old %> KB)</p>
        <% else %>
          <p><b><%= $tMjInBundle %></b></p>
        <% fi %>
        <% if [ "$mj_filesize_new" -le "$available_space" ]; then %>
          <form action="/cgi-bin/majestic-github.cgi" method="post">
            <p><button class="btn btn-warning"><%= $tButtonInstallUpdate %></button></p>
          </form>
        <% else %>
          <div class="alert alert-warning"><%= $tMjNoSpace %></div>
        <% fi %>
        </div>
        <div class="alert alert-light mb-0">
        <% if [ -z "$mj_config_diff" ]; then %>
          <p><b><%= $tMjConfigUnchanged %></b></p>
          <p class="mb-0"><a href="/cgi-bin/majestic-settings-general.cgi"><%= $tMjConfigEdit %></a></p>
        <% else %>
          <p><b><%= $tMjConfigChanged %></b></p>
          <p><a href="/cgi-bin/majestic-config-compare.cgi"><%= $tMjConfigSeeChanges %></a></p>
          <div class="alert alert-danger mb-0">
            <p><b><%= $tMjConfigReset %></b></p>
            <p><%= $tMjConfigResetInfo %></p>
            <p class="mb-0">
              <a class="btn btn-primary" href="/cgi-bin/majestic-config-backup.cgi"><%= $tMjConfigBackup %></a>
              <a class="btn btn-danger" href="/cgi-bin/majestic-config-reset.cgi" title="<%= $tMjConfigResetTitle %>"><%= $tMjConfigReset %></a>
            </p>
          </div>
        <% fi %>
        </div>
      </div>
    </div>
  </div>
  <div class="col">
    <div class="card h-100">
      <div class="card-header"><%= $tHeaderCamera %></div>
      <div class="card-body">
        <a class="btn btn-warning" href="/cgi-bin/reboot.cgi"><%= $tRebootCamera %></a>
      </div>
    </div>
  </div>
  <div class="col">
    <div class="card h-100">
      <div class="card-header"><%= $tHeaderUploadKernel %></div>
      <div class="card-body">
        <form action="/cgi-bin/firmware-upload-kernel.cgi" method="post" enctype="multipart/form-data">
          <div class="row mb-3">
            <label class="col-md-3 form-label" for="upfile"><%= $tKernelFile %></label>
            <div class="col-md-9">
              <input class="form-control" type="file" name="upfile">
            </div>
          </div>
          <button type="submit" class="btn btn-danger"><%= $tButtonUploadFile %></button>
        </form>
      </div>
    </div>
  </div>
  <div class="col">
    <div class="card h-100">
      <div class="card-header"><%= $tHeaderUploadRootfs %></div>
      <div class="card-body">
        <form action="/cgi-bin/firmware-upload-rootfs.cgi" method="post" enctype="multipart/form-data">
          <div class="row mb-3">
            <label class="col-md-3 form-label" for="upfile"><%= $tRootfsFile %></label>
            <div class="col-md-9">
              <input class="form-control" type="file" name="upfile">
            </div>
          </div>
          <button type="submit" class="btn btn-danger"><%= $tButtonUploadFile %></button>
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
