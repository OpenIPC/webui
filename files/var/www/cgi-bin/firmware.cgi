#!/usr/bin/haserl
<%in _common.cgi %>
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
<%in _header.cgi %>
<div class="alert alert-danger">
<h6><%= $tMsgDestructiveActions %></h6>
<p class="mb-0"><%= $tMsgKnowWhatYouDo %></p>
</div>
<div class="row row-cols-1 row-cols-md-2 row-cols-xl-3 g-3 mb-3">
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_firmware_1 %></div>
<div class="card-body">
<dl class="row small">
<dt class="col-4"><%= $t_firmware_2 %></dt>
<dd class="col-8 text-end"><%= $fw_version %></dd>
<dt class="col-4"><%= $t_firmware_3 %></dt>
<dd class="col-8 text-end" id="firmware-master-ver"><%= $fw_date %></dd>
</dl>
<div class="alert alert-light">
<h6><%= $t_firmware_4 %></h6>
<form action="/cgi-bin/firmware-update.cgi" method="post" autocomplete="off">
<div class="mb-2 boolean form-check">
<input type="hidden" name="fw_kernel" id="fw_kernel-false" value="false">
<input type="checkbox" name="fw_kernel" id="fw_kernel" value="true" class="form-check-input" checked>
<label for="fw_kernel" class="form-check-label"><%= $tL_fw_kernel %></label>
</div>
<div class="mb-2 boolean form-check">
<input type="hidden" name="fw_rootfs" id="fw_rootfs-false" value="false">
<input type="checkbox" name="fw_rootfs" id="fw_rootfs" value="true" class="form-check-input" checked>
<label for="fw_rootfs" class="form-check-label"><%= $tL_fw_rootfs %></label>
</div>
<div class="mb-2 boolean form-check">
<input type="hidden" name="fw_reset" id="fw_reset-false" value="false">
<input type="checkbox" name="fw_reset" id="fw_reset" value="true" class="form-check-input">
<label for="fw_reset" class="form-check-label"><%= $tL_fw_reset %></label>
</div>
<div class="mb-2 boolean form-check">
<input type="hidden" name="fw_noreboot" id="fw_noreboot-false" value="false">
<input type="checkbox" name="fw_noreboot" id="fw_noreboot" value="true" class="form-check-input">
<label for="fw_noreboot" class="form-check-label"><%= $tL_fw_noreboot %></label>
</div>
<div class="mb-2 boolean form-check">
<input type="hidden" name="fw_enforce" id="fw_enforce-false" value="false">
<input type="checkbox" name="fw_enforce" id="fw_enforce" value="true" class="form-check-input">
<label for="fw_enforce" class="form-check-label"><%= $tL_fw_enforce %></label>
</div>
<button type="submit" class="btn btn-warning mt-3" ><%= $t_firmware_5 %></button>
</form>
</div>
<%in reset-firmware.cgi %>
</div>
</div>
</div>
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_firmware_6 %></div>
<div class="card-body">
<dl class="row small">
<dt class="col-4"><%= $t_firmware_7 %></dt>
<dd class="col-8 text-end"><%= $ui_version %></dd>
<dt class="col-4"><%= $t_firmware_8 %></dt>
<dd class="col-8 text-end" id="microbe-web-master-ver"></dd>
<dt class="col-4"><%= $t_firmware_9 %></dt>
<dd class="col-8 text-end" id="microbe-web-dev-ver"></dd>
</dl>
<div class="alert alert-light">
<h6><%= $t_firmware_a %></h6>
<form action="/cgi-bin/webui-update.cgi" method="post" autocomplete="off">
<div class="mb-2 select">
<label for="web_version" class="form-label"><%= $t_firmware_y %></label>
<div class="input-group">
<select class="form-select" id="web_version" name="web_version">
<option value="master">master (Stable)</option>
<option value="dev">dev (Unstable)</option>
</select>
</div>
</div>
<div class="mb-2 boolean form-check">
<input type="hidden" name="web_enforce" id="web_enforce-false" value="false">
<input type="checkbox" name="web_enforce" id="web_enforce"  value="true" class="form-check-input">
<label for="web_enforce" class="form-check-label"><%= $tL_fw_enforce %></label>
</div>
<button type="submit" class="btn btn-warning mt-3"><%= $t_firmware_b %></button>
</form>
</div>
</div>
</div>
</div>
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_firmware_c %></div>
<div class="card-body">
<dl class="row small">
<dt class="col-4"><%= $t_firmware_d %></dt>
<dd class="col-8 text-end"></dd>
<dt class="col-4"><%= $t_firmware_e %></dt>
<dd class="col-8 text-end"></dd>
</dl>
<div class="alert alert-light">
<h6><% if [ -f "/overlay/root/${mj_mj_bin_file}" ]; then %>
<%= $t_firmware_f %> (<%= $mj_filesize_overlay %> KB)
<% else %>
<%= $t_firmware_g %>
<% fi %></h6>
<% if [ "$mj_filesize_new" -le "$available_space" ]; then %>
<form action="/cgi-bin/majestic-update.cgi" method="post" autocomplete="off">
<button type="submit" class="btn btn-warning"><%= $t_firmware_h %></button>
</form>
<% else %>
<div class="alert alert-warning"><%= $t_firmware_i %></div>
<% fi %>
</div>
<% if [ -z "$(diff /rom/etc/majestic.yaml /etc/majestic.yaml)" ]; then %>
<div class="alert alert-light">
<h6><%= $t_firmware_j %></h6>
<a href="/cgi-bin/majestic-settings.cgi"><%= $t_firmware_k %></a>
</div>
<% else %>
<div class="alert alert-light">
<h6><%= $t_firmware_l %></h6>
<a href="/cgi-bin/majestic-config-compare.cgi"><%= $t_firmware_m %></a>
</div>
<div class="alert alert-danger">
<h6><%= $t_firmware_n %></h6>
<p><%= $t_firmware_o %></p>
<a class="btn btn-primary me-2" href="/cgi-bin/majestic-config-backup.cgi"><%= $t_firmware_p %></a>
<a class="btn btn-danger" href="/cgi-bin/majestic-config-reset.cgi" title="<%= $t_firmware_r %>"><%= $t_firmware_q %></a>
</div>
<% fi %>
</div>
</div>
</div>
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_firmware_s %></div>
<div class="card-body">
<% button_reboot %>
</div>
</div>
</div>
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_firmware_u %></div>
<div class="card-body">
<form action="/cgi-bin/firmware-upload-kernel.cgi" method="post" enctype="multipart/form-data" autocomplete="off">
<div class="mb-2 file">
<label for="kernel_file" class="form-label"><%= $tL_kernel_file %></label>
<input type="file" name="kernel_file" id="kernel_file" class="form-control">
</div>
<button type="submit" class="btn btn-danger mt-3"><%= $t_firmware_v %></button>
</form>
</div>
</div>
</div>
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_firmware_w %></div>
<div class="card-body">
<form action="/cgi-bin/firmware-upload-rootfs.cgi" method="post" enctype="multipart/form-data" autocomplete="off">
<div class="mb-2 file">
<label for="rootfs_file" class="form-label"><%= $tL_rootfs_file %></label>
<input type="file" name="rootfs_file" id="rootfs_file" class="form-control">
</div>
<button type="submit" class="btn btn-danger mt-3"><%= $t_firmware_x %></button>
</form>
</div>
</div>
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
  oReq.send();
}

window.addEventListener('load', checkUpdates);
</script>
<%in p/footer.cgi %>
