#!/usr/bin/haserl
<%
command="curl -skI https://codeload.github.com/OpenIPC/microbe-web/zip/refs/heads/themactep-dev"
output=$($command 2>&1)
result=$?
if [ "0" -ne "$result" ]; then
  webui_gh_etag="[unknown]"
else
  webui_gh_headers="$output"
  webui_gh_etag=$(echo "$webui_gh_headers" | grep "ETag:" | cut -d " " -f2 | sed 's/"//g')
fi

webui_local_etag=$(cat /var/www/.etag)
[ -z "$webui_local_etag" ] && webui_local_etag="[unknown]"

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
    <div class="card mb-3 danger">
      <div class="card-header">Firmware</div>
      <div class="card-body">
        <form action="/cgi-bin/firmware-update.cgi" method="post">
          <p><input type="checkbox" name="reset" value="true">
            <label for="reset">Reset settings after upgrade.</label></p>
          <a class="btn btn-danger float-end">Reset overlay</a>
          <input type="submit" class="btn btn-danger" value="Upgrade Firmware from GitHub">
        </form>
      </div>
    </div>

    <div class="card mb-3 danger">
      <div class="card-header">Web UI</div>
      <div class="card-body">
        <dl>
          <dt>Local version</dt>
          <dd class="small"><%= $webui_local_etag %></dd>
          <dt>GitHub version</dt>
          <dd class="small"><%= $webui_gh_etag %></dd>
        </dl>
        <form action="/cgi-bin/web-ui-update.cgi" method="post">
          <input type="submit" class="btn btn-danger" value="Update Web UI from GitHub">
        </form>
      </div>
    </div>

    <div class="card mb-3 danger">
      <div class="card-header">Majestic</div>
      <div class="card-body">
        <% if [ -z "$majestic_diff" ]; then %>
          <p><b>Majestic uses the original configuration.</b> <a href="/cgi-bin/majestic.cgi">Change settings.</a></p>
        <% else %>
          <p><b>Majestic uses custom configuration.</b> <a href="/cgi-bin/majestic-diff.cgi">See changes.</a></p>
        <% fi %>
        <p class="mb-0">
          <% if [ ! -z "$majestic_diff" ]; then %>
            <a class="btn btn-danger float-end" href="/cgi-bin/majestic-reset.cgi">Reset configuration</a>
          <% fi %>
          <a class="btn btn-danger" href="/cgi-bin/github-majestic.cgi">Update Majestic from GitHub</a>
        </p>
      </div>
    </div>

  </div>
  <div class="col">

    <div class="card mb-3 danger">
      <div class="card-header">Camera</div>
      <div class="card-body">
        <p class="mb-0"><a class="btn btn-danger" href="/cgi-bin/reboot.cgi">Reboot camera</a></p>
      </div>
    </div>

    <div class="card mb-3 danger">
      <div class="card-header">Upload kernel</div>
      <div class="card-body">
        <form action="/cgi-bin/firmware-upload-kernel.cgi" method="post" enctype="multipart/form-data">
          <div class="row">
            <div class="col-12 mb-3"><label for="upfile">kernel file</label></div>
            <div class="col-12 mb-3"><input type="file" name="upfile"></div>
          </div>
          <p class="mb-0"><input type="submit" class="btn btn-danger" value="Upload kernel file"></p>
        </form>
      </div>
    </div>

    <div class="card mb-3 danger">
      <div class="card-header">Upload rootfs</div>
      <div class="card-body">
        <form action="/cgi-bin/firmware-upload-rootfs.cgi" method="post" enctype="multipart/form-data">
          <div class="row">
            <div class="col-12 mb-3"><label for="upfile">rootfs file</label></div>
            <div class="col-12 mb-3"><input type="file" name="upfile"></div>
          </div>
          <p class="mb-0"><input type="submit" class="btn btn-danger" value="Upload rootfs file"></p>
        </form>
      </div>
    </div>
  </div>
</div>

<%in _footer.cgi %>
