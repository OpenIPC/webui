#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Firmware"

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

mj_meta_file=/tmp/mj_meta.txt

update_meta() {
  # re-download metafile if older than 1 hour
  mj_meta_url="http://openipc.s3-eu-west-1.amazonaws.com/majestic.${soc_family}.${fw_variant}.master.tar.meta"
  mj_meta_file_timestamp=$(date +%s --date "$(ls -lc --full-time $mj_meta_file | xargs | cut -d' ' -f6,7)")
  mj_meta_file_expiration=$(( $(date +%s) + 3600 ))
  [ -f "$mj_meta_file" ] && [ "$mj_meta_file_timestamp" -le "$mj_meta_file_expiration" ] && return

  rm $mj_meta_file
  if [ "200" = $(curl $mj_meta_url -s -f -w %{http_code} -o /dev/null) ]; then
    curl -s $mj_meta_url -o $mj_meta_file
  fi
}

update_meta

mj_version_fw=$(/rom${mj_bin_file} -v)

if [ -f "$mj_meta_file" ]; then
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
else
  mj_version_new="unavailable"
fi

fw_kernel="true"
fw_rootfs="true"
%>
<%in p/header.cgi %>

<h4 class="text-danger my-4">Attention: Destructive Actions! Make sure you know what you are doing.</h4>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
  <div class="col">
    <h3>Firmware</h3>
    <dl class="small list">
      <dt>Installed</dt>
      <dd><%= $fw_version %></dd>
      <dt>On GitHub</dt>
      <dd id="firmware-master-ver"><%= $fw_date %></dd>
    </dl>

    <h4>Install update</h4>
    <form action="firmware-update.cgi" method="post">
      <p class="boolean form-check">
        <input type="hidden" name="fw_kernel" id="fw_kernel-false" value="false">
        <input type="checkbox" name="fw_kernel" id="fw_kernel" checked value="true" class="form-check-input">
        <label for="fw_kernel" class="form-label">Upgrade kernel.</label>
      </p>
      <p class="boolean form-check">
        <input type="hidden" name="fw_rootfs" id="fw_rootfs-false" value="false">
        <input type="checkbox" name="fw_rootfs" id="fw_rootfs" checked value="true" class="form-check-input">
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
      <p class="mt-2"><input type="submit" class="btn btn-warning" value="<%= $t_btn_update %>"></p>
    </form>
  </div>

  <div class="col">
    <h3>Kernel & RootFS</h3>
    <form action="firmware-upload-parts.cgi" method="post" enctype="multipart/form-data">
      <p class="select">
        <label for="parts_type" class="form-label">Type of binary file</label>
        <select class="form-select" id="parts_type" name="parts_type" required>
          <option value="">Choose...</option>
          <option value="kernel">Kernel</option>
          <option value="rootfs">RootFS</option>
        </select>
      </p>
      <p class="file">
        <label for="parts_file" class="form-label">Binary file</label>
        <input type="file" id="parts_file" name="parts_file" class="form-control" required>
      </p>
      <p class="mt-2"><input type="submit" class="btn btn-warning" value="<%= $t_btn_upload %>"></p>
    </form>
  </div>

  <div class="col">
    <h3>Majestic</h3>
    <dl class="small list">
      <dt>Installed</dt>
      <dd><%= $mj_version %></dd>
      <dt>Bundled</dt>
      <dd><%= $mj_version_fw %></dd>
      <dt>On GitHub</dt>
      <dd><%= $mj_version_new %></dd>
    </dl>

    <% if [ -z "$(diff /rom/etc/majestic.yaml /etc/majestic.yaml)" ]; then %>
      <p>Majestic uses original configuration.</p>
      <p><a href="majestic-settings.cgi">Make changes.</a></p>
    <% else %>
      <p>Majestic uses custom configuration.</p>
      <p><a href="majestic-config-compare.cgi" class="btn btn-primary">See difference</a></p>
    <% fi %>

    <% if [ -f "$mj_meta_file" ]; then %>
      <% if [ "$mj_filesize_new" -le "$available_space" ]; then %>
        <p><a href="majestic-update.cgi" class="btn btn-warning"><%= $t_btn_update %></a></p>
      <% else %>
        <p class="alert alert-danger">Not enough space to update Majestic.</p>
      <% fi %>

      <% if [ -f "/overlay/root/${mj_mj_bin_file}" ]; then %>
        <div class="alert alert-warning">
          <p>More recent version of Majestic found in overlay partition.
           It takes <%= $mj_filesize_overlay %> KB of space.</p>
          <form action="<%= $SCRIPT_NAME %>" method="post">
            <input type="hidden" name="action" value="rmmj">
            <p class="mb-0"><input type="submit" value="Revert to bundled version" class="btn btn-warning"></p>
          </form>
        </div>
      <% fi %>
    <% fi %>
  </div>
</div>

<%in p/footer.cgi %>
