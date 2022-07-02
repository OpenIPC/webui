#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Majestic"

# NB! size in allocated blocks.

mj_filesize_fw=$(ls -s $mj_bin_file | xargs | cut -d' ' -f1)

mj_bin_file_overlay="${overlay_root}${mj_bin_file}"

if [ -f "$mj_bin_file_overlay" ]; then
  mj_filesize_overlay=$(ls -s $mj_bin_file_overlay | xargs | cut -d' ' -f1)
  mj_filesize_old=$mj_filesize_overlay
else
  mj_filesize_old=$mj_filesize_fw
fi

mj_meta_file=/tmp/mj_meta.txt

update_meta() {
  # re-download metafile if older than 1 hour
  mj_meta_url="http://openipc.s3-eu-west-1.amazonaws.com/majestic.${soc_family}.${fw_variant}.master.tar.meta"

  if [ -f "$mj_meta_file" ]; then
    mj_meta_file_timestamp=$(time_epoch "$(ls -lc --full-time $mj_meta_file | xargs | cut -d' ' -f6,7)")
    mj_meta_file_expiration=$(( $(time_epoch) + 3600 ))
    [ "$mj_meta_file_timestamp" -le "$mj_meta_file_expiration" ] && return
    rm $mj_meta_file
  fi

  if [ "200" = $(curl $mj_meta_url -s -f -w %{http_code} -o /dev/null) ]; then
    curl -s $mj_meta_url -o $mj_meta_file
  fi
}

update_meta

mj_version_fw=$(/rom${mj_bin_file} -v)

mj_version_ol="<span class=\"text-secondary\">- not installed in overlay -</span>"
[ -f "$mj_bin_file_overlay" ] && mj_version_ol=$($mj_bin_file_overlay -v)

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
  free_space=$(df | grep ${overlay_root} | xargs | cut -d' ' -f4)
  available_space=$(( ${free_space:=0} + ${mj_filesize_overlay:=0} ))
else
  mj_version_new="unavailable"
fi
%>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
  <div class="col">
    <h3>Version</h3>
    <dl class="list small">
      <dt>Bundled</dt>
      <dd><%= $mj_version_fw %></dd>
      <dt>In overlay</dt>
      <dd><%= $mj_version_ol %></dd>
      <dt>On GitHub</dt>
      <dd><%= $mj_version_new %></dd>
    </dl>
  </div>
  <div class="col">
    <h3>Configuration</h3>
    <% if [ -z "$(diff /rom/etc/majestic.yaml /etc/majestic.yaml)" ]; then %>
      <p>Majestic uses original configuration.</p>
      <p><a href="majestic-settings.cgi">Make changes.</a></p>
    <% else %>
      <p>Majestic uses custom configuration.</p>
      <p><a href="majestic-config-compare.cgi" class="btn btn-primary">See difference</a></p>
    <% fi %>
  </div>
  <div class="col">
    <h3>Update</h3>
    <% if [ -f "$mj_meta_file" ]; then %>
      <% if [ "$mj_filesize_new" -le "$available_space" ]; then %>
        <p><a href="majestic-update.cgi" class="btn btn-warning"><%= $t_btn_update %></a></p>
      <% else %>
        <div class="alert alert-danger">
          <p class="mb-1"><b>Not enough space to update Majestic!</b></p>
          <p class="mb-0">Update requires <%= $mj_filesize_new %>K,
          but only <%= $available_space %>K is available in overlay,
          as <%= $free_space %>K of unallocated space,
          plus <%= ${mj_filesize_overlay:=0} %>K size of Majestic installed in overlay.</p>
        </div>
      <% fi %>
      <% if [ -f "$mj_bin_file_overlay" ]; then %>
        <div class="alert alert-warning">
          <p>More recent version of Majestic found in overlay partition.
           It takes <%= $mj_filesize_overlay %> KB of space.</p>
          <form action="<%= $SCRIPT_NAME %>" method="post">
            <% field_hidden "action" "rmmj" %>
            <% button_submit "Revert to bundled version" "warning" %>
          </form>
        </div>
      <% fi %>
    <% fi %>
  </div>
</div>

<%in p/footer.cgi %>
