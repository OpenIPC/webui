#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="$t_firmware_0"

# firmware data
fw_date=$(date -D "%a, %d %b %Y %T GMT" +"2.2.%m.%d" --date "$(curl -ILs https://github.com/OpenIPC/firmware/releases/download/latest/openipc.${soc}-br.tgz | grep Last-Modified | cut -d' ' -f2-)")

# NB! size in allocated blocks.
mj_filesize_fw=$(ls -s $mj_bin_file | xargs | cut -d' ' -f1)
if [ -f "/overlay/$mj_bin_file" ]; then
  mj_filesize_overlay=$(ls -s /overlay/$mj_bin_file | xargs | cut -d' ' -f1)
  mj_filesize_old=$mj_filesize_overlay
else
  mj_filesize_old=$mj_filesize_fw
fi

# re-download metafile if older than 1 hour
mj_meta_url="http://openipc.s3-eu-west-1.amazonaws.com/majestic.${soc_family}.${fw_variant}.master.tar.meta"
mj_meta_file=/tmp/mj_meta.txt
dl_mj_meta() { curl -s $mj_meta_url -o $mj_meta_file; }
[ ! -f "$mj_meta_file" ] && dl_mj_meta
mj_meta_file_timestamp=$(date +%s --date "$(ls -lc --full-time $mj_meta_file | xargs | cut -d' ' -f6,7)")
mj_meta_file_expiration=$(( $(date +%s) + 3600 ))
[ "$mj_meta_file_timestamp" -gt "$mj_meta_file_expiration" ] && dl_mj_meta

# parse version, date and file size
if [ "$(wc -l $mj_meta_file | cut -d' ' -f1)" = "1" ]; then
  mj_filesize_new=$(sed -n 1p $mj_meta_file)
else
  mj_version_new=$(sed -n 1p $mj_meta_file)
  mj_filesize_new=$(sed -n 2p $mj_meta_file)
fi
# NB! size in bytes, but since blocks are 1024 bytes each, we are safe here for now.
mj_filesize_new=$(( ($mj_filesize_new + 1024) / 1024 )) # Rounding up by priming, since $(()) sucks at floats.

free_space=$(df | grep /overlay | xargs | cut -d' ' -f4)
available_space=$(( $free_space + $mj_filesize_overlay - 1 ))

fw_kernel="true"
fw_rootfs="true"
%>
<%in p/header.cgi %>

<h4 class="text-danger my-4"><%= $tMsgDestructiveActions %></h4>

<div class="row row-cols-1 row-cols-md-2 row-cols-xl-3 g-4">
  <div class="col">
    <h3><%= $t_firmware_1 %></h3>
    <dl class="small list">
      <dt><%= $t_firmware_2 %></dt>
      <dd><%= $fw_version %></dd>
      <dt><%= $t_firmware_3 %></dt>
      <dd id="firmware-master-ver"><%= $fw_date %></dd>
    </dl>
  
    <h4><%= $t_firmware_4 %></h4>
    <form action="/cgi-bin/firmware-update.cgi" method="post">
      <p class="boolean form-check">
        <input type="hidden" name="fw_kernel" id="fw_kernel-false" value="false">
        <input type="checkbox" name="fw_kernel" id="fw_kernel" checked="true" value="true" class="form-check-input">
        <label for="fw_kernel" class="form-label">Upgrade kernel.</label>
      </p>
      <p class="boolean form-check">
        <input type="hidden" name="fw_rootfs" id="fw_rootfs-false" value="false">
        <input type="checkbox" name="fw_rootfs" id="fw_rootfs" checked="true" value="true" class="form-check-input">
        <label for="fw_rootfs" class="form-label">Upgrade rootfs.</label>
      </p>
      <p class="boolean form-check">
        <input type="hidden" name="fw_reset" id="fw_reset-false" value="false">
        <input type="checkbox" name="fw_reset" id="fw_reset" value="true" class="form-check-input">
        <label for="fw_reset" class="form-label">Reset firmware.</label>
      </p>
      <p class="boolean form-check">
        <input type="hidden" name="fw_noreboot" id="fw_noreboot-false" value="false">
        <input type="checkbox" name="fw_noreboot" id="fw_noreboot" value="true" class="form-check-input">
        <label for="fw_noreboot" class="form-label">Do not reboot after upgrade.</label>
      </p>
      <p class="boolean form-check">
        <input type="hidden" name="fw_enforce" id="fw_enforce-false" value="false">
        <input type="checkbox" name="fw_enforce" id="fw_enforce" value="true" class="form-check-input">
        <label for="fw_enforce" class="form-label">Install even if matches the existing version.</label>
      </p>
      <p class="button submit mt-2"><input type="submit" class="btn btn-warning" value="<%= $t_btn_update %>"></p>
    </form>
  
    <h3><%= $t_firmware_u %></h3>
    <form action="/cgi-bin/firmware-upload-parts.cgi" method="post" enctype="multipart/form-data">
      <div class="input-group mb-3">
        <input type="file" id="parts_file" name="parts_file" class="form-control" style="width:70%">
        <select class="form-select" id="parts_type" name="parts_type" style="width:6rem">
          <option selected>Choose...</option>
          <option value="kernel">Kernel</option>
          <option value="rootfs">RootFS</option>
        </select>
      </div>
    <%
#      field_file "kernel_file" "form-control-sm"
#      field_file "rootfs_file" "form-control-sm"
      button_submit "$t_btn_upload"
    _form
  %>

</div>

<div class="col">
  <h3><%= $t_firmware_c %></h3>
  <dl class="small list">
    <dt><%= $t_firmware_d %></dt>
    <dd><%= $mj_version %></dd>
    <dt><%= $t_firmware_e %></dt>
    <dd><%= $mj_version_new %></dd>
  </dl>

  <%#= $t_firmware_g %>
  <% if [ -f "/overlay/root/${mj_mj_bin_file}" ]; then %>
  <p class="alert alert-info"><%= $t_firmware_f %> (<%= $mj_filesize_overlay %> KB)</p>
  <% fi %>

  <% if [ "$mj_filesize_new" -le "$available_space" ]; then %>
  <p><a href="/cgi-bin/majestic-update.cgi" class="btn btn-warning"><%= $t_btn_update %></a></p>
  <% else %>
  <p class="alert alert-warning"><%= $t_firmware_i %></p>
  <% fi %>

  <% if [ -z "$(diff /rom/etc/majestic.yaml /etc/majestic.yaml)" ]; then %>
  <h5><%= $t_firmware_j %></h5>
  <p><a href="/cgi-bin/majestic-settings.cgi"><%= $t_firmware_k %></a></p>
<% else %>
  <h5><%= $t_firmware_l %></h5>
  <p><a href="/cgi-bin/majestic-config-compare.cgi" class="btn btn-primary"><%= $t_firmware_m %></a></p>

  <h3><%= $t_firmware_6 %></h3>
  <dl class="small list">
    <dt><%= $t_firmware_7 %></dt>
    <dd><%= $ui_version %></dd>
    <dt><%= $t_firmware_8 %></dt>
    <dd id="microbe-web-master-ver"></dd>
    <dt><%= $t_firmware_9 %></dt>
    <dd id="microbe-web-dev-ver"></dd>
  </dl>

  <h4><%= $t_firmware_a %></h4>
  <form action="/cgi-bin/webui-update.cgi" method="post">
    <p class="select input-group">
      <label for="web_version" class="input-group-text">Branch</label>
      <select class="form-select" id="web_version" name="web_version">
        <option value="master">Stable</option>
        <option value="dev">Development</option>
      </select>
    </p>
    <p class="boolean form-check">
      <input type="checkbox" name="web_enforce" id="web_enforce" value="true" class="form-check-input">
      <label for="web_enforce" class="form-label">Install even if matches the existing version.</label>
    </p>
    <p class="button submit mt-2">
      <input type="submit" class="btn btn-warning" value="<%= $t_btn_update %>">
    </p>
  </form>
</div>

<div class="col">
  <div class="alert alert-danger">
    <h4>Reboot camera</h4>
    <p>Reboot camera to apply new settings. That will also delete all data on partitions mounted into system memory, like /tmp and such.</p>
    <% button_reboot %>
  </div>

  <%in p/reset-firmware.cgi %>

  <div class="alert alert-danger">
    <h4><%= $t_firmware_n %></h4>
    <p><%= $t_firmware_o %></p>
    <p class="d-flex gap-2 mb-0">
      <a class="btn btn-primary" href="/cgi-bin/majestic-config-backup.cgi"><%= $t_firmware_p %></a>
      <a class="btn btn-danger" href="/cgi-bin/majestic-config-reset.cgi" title="<%= $t_firmware_r %>"><%= $t_firmware_q %></a>
    </p>
  </div>
<% fi %>
</div>
</div>

<script>
const GH_URL="https://github.com/OpenIPC/";
const GH_API="https://api.github.com/repos/OpenIPC/";

function checkUpdates() {
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
    link.href = GH_URL + repo + '/commits/' + branch;
    link.target = '_blank';
    link.textContent = branch + '+' + sha_short + ', ' + date;
    const el = $('#' + repo + '-' + branch + '-ver').appendChild(link);
  });
  oReq.open("GET", GH_API + repo + '/branches/' + branch);
  oReq.setRequestHeader("Authorization", "Basic " + btoa("<%= "${GITHUB_USERNAME}:${GITHUB_TOKEN}" %>"));
  oReq.send();
}

window.addEventListener('load', checkUpdates);
</script>
<%in p/footer.cgi %>
