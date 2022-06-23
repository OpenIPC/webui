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
<div class="alert alert-danger">
<h6><%= $tMsgDestructiveActions %></h6>
<p class="mb-0"><%= $tMsgKnowWhatYouDo %></p>
</div>
<div class="row row-cols-1 row-cols-md-2 row-cols-xl-3 g-4">
<div class="col">
<h3><%= $t_firmware_1 %></h3>
<dl class="small list">
<dt><%= $t_firmware_2 %></dt>
<dd><%= $fw_version %></dd>
<dt><%= $t_firmware_3 %></dt>
<dd id="firmware-master-ver"><%= $fw_date %></dd>
</dl>
<div class="alert alert-warning">
<h6><%= $t_firmware_4 %></h6>
<form action="/cgi-bin/firmware-update.cgi" method="post">
<%
field_checkbox "fw_kernel"
field_checkbox "fw_rootfs"
field_checkbox "fw_reset"
field_checkbox "fw_noreboot"
field_checkbox "fw_enforce"
button_submit "$t_firmware_5" "warning"
%>
</form>
</div>
<%in reset-firmware.cgi %>
</div>
<div class="col">
<h3><%= $t_firmware_6 %></h3>
<dl class="small list">
<dt><%= $t_firmware_7 %></dt>
<dd><%= $ui_version %></dd>
<dt><%= $t_firmware_8 %></dt>
<dd id="microbe-web-master-ver"></dd>
<dt><%= $t_firmware_9 %></dt>
<dd id="microbe-web-dev-ver"></dd>
</dl>
<div class="alert alert-warning">
<h6><%= $t_firmware_a %></h6>
<form action="/cgi-bin/webui-update.cgi" method="post">
<%
field_select "web_version"
field_checkbox "web_enforce"
button_submit "$t_firmware_b" "warning"
%>
</form>
</div>
</div>
<div class="col">
<h3><%= $t_firmware_c %></h3>
<dl class="small list">
<dt><%= $t_firmware_d %></dt>
<dd><%= $mj_version %></dd>
<dt><%= $t_firmware_e %></dt>
<dd><%= $mj_version_new %></dd>
</dl>

<div class="alert alert-info">
<h6><% if [ -f "/overlay/root/${mj_mj_bin_file}" ]; then %>
<%= $t_firmware_f %> (<%= $mj_filesize_overlay %> KB)
<% else %>
<%= $t_firmware_g %>
<% fi %></h6>

<% if [ "$mj_filesize_new" -le "$available_space" ]; then %>
<a href="/cgi-bin/majestic-update.cgi" class="btn btn-warning"><%= $t_firmware_h %></a>
<% else
  echo $t_firmware_i
fi %>
</div>

<% if [ -z "$(diff /rom/etc/majestic.yaml /etc/majestic.yaml)" ]; then %>
<div class="alert alert-light">
<h6><%= $t_firmware_j %></h6>
<p><a href="/cgi-bin/majestic-settings.cgi"><%= $t_firmware_k %></a></p>
</div>
<% else %>
<div class="alert alert-light">
<h6><%= $t_firmware_l %></h6>
<p><a href="/cgi-bin/majestic-config-compare.cgi"><%= $t_firmware_m %></a></p>
</div>

<div class="alert alert-danger">
<h6><%= $t_firmware_n %></h6>
<p><%= $t_firmware_o %></p>
<p>
<a class="btn btn-primary me-2" href="/cgi-bin/majestic-config-backup.cgi"><%= $t_firmware_p %></a>
<a class="btn btn-danger" href="/cgi-bin/majestic-config-reset.cgi" title="<%= $t_firmware_r %>"><%= $t_firmware_q %></a>
</p>
</div>
<% fi %>
</div>
<div class="col">
<h3><%= $t_firmware_s %></h3>
<% button_reboot %>
</div>
<div class="col">
<h3><%= $t_firmware_u %></h3>
<form action="/cgi-bin/firmware-upload-kernel.cgi" method="post" enctype="multipart/form-data">
<%
field_file "kernel_file"
button_submit "$t_firmware_v"
%>
</form>
</div>
<div class="col">
<h3><%= $t_firmware_w %></h3>
<form action="/cgi-bin/firmware-upload-rootfs.cgi" method="post" enctype="multipart/form-data">
<%
field_file "rootfs_file"
button_submit "$t_firmware_x"
%>
</form>
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
