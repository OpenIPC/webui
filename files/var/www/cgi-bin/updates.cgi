#!/usr/bin/haserl
content-type: text/html

<%
gh_headers=$(curl --silent --head https://codeload.github.com/OpenIPC/microbe-web/zip/refs/heads/themactep-dev)
webui_github_etag=$(echo "$gh_headers" | grep "ETag:" | cut -d " " -f2 | sed 's/"//g')
webui_local_etag=$(cat /var/www/.etag)
[ -z "$webui_local_etag" ] && webui_local_etag="unknown"
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
      <div class="card-header">Upgrade Firmware from GitHub</div>
      <div class="card-body">
        <form action="/cgi-bin/github-firmware.cgi" method="post">
          <input type="hidden" name="action" value="github">
          <p><input type="checkbox" name="reset" id="reset" value="true"> <label for="reset">Reset settings after upgrade.</label></p>
          <p><input type="submit" class="btn btn-danger" value="Upgrade Firmware"></p>
        </form>
      </div>
    </div>

    <div class="card mb-3 danger">
      <div class="card-header">Update Web UI from GitHub</div>
      <div class="card-body">
        <dl>
          <dt>Installed version</dt>
          <dd class="small"><%= $webui_local_etag %></dd>
          <dt>Available version</dt>
          <dd class="small"><%= $webui_github_etag %></dd>
        </dl>
        <form action="/cgi-bin/github-webui.cgi" method="post">
          <p><input type="submit" class="btn btn-danger" value="Update Web UI"></p>
        </form>
      </div>
    </div>

    <div class="card mb-3 danger">
      <div class="card-header">Reset Majestic configuration</div>
      <div class="card-body">
        <p><a href="/cgi-bin/majestic-diff.cgi">See how recent configuration differs from the original one.</a></p>
        <form action="/cgi-bin/reset.cgi" method="post">
          <input type="hidden" name="action" value="reset">
          <p><input type="submit" class="btn btn-danger" value="Reset Majestic Configuration"></p>
        </form>
      </div>
    </div>

  </div>
  <div class="col">

    <div class="card mb-3 danger">
      <div class="card-header">Reboot camera</div>
      <div class="card-body">
        <p><a class="btn btn-danger" href="/cgi-bin/reboot.cgi">Reboot</a></p>
      </div>
    </div>

    <div class="card mb-3 danger">
      <div class="card-header">Upload kernel</div>
      <div class="card-body">
        <form action="/cgi-bin/upload.cgi" method="post" enctype="multipart/form-data">
          <input type="hidden" name="action" value="kernel">
          <div class="row">
            <div class="col-12 mb-3"><label for="upfile">kernel file</label></div>
            <div class="col-12 mb-3"><input type="file" name="upfile"></div>
          </div>
          <p><input type="submit" class="btn btn-danger" value="Upload File"></p>
        </form>
      </div>
      <div class="card-footer bg-black text-white">Sorry, some things aren't working yet.</div>
    </div>

    <div class="card mb-3 danger">
      <div class="card-header">Upload rootfs</div>
      <div class="card-body">
        <form action="/cgi-bin/upload.cgi" method="post" enctype="multipart/form-data">
          <input type="hidden" name="action" value="rootfs">
          <div class="row">
            <div class="col-12 mb-3"><label for="upfile">rootfs file</label></div>
            <div class="col-12 mb-3"><input type="file" name="upfile"></div>
          </div>
          <p><input type="submit" class="btn btn-danger" value="Upload File"></p>
        </form>
      </div>
      <div class="card-footer bg-black text-white">Sorry, some things aren't working yet.</div>
    </div>
  </div>
</div>

<%in _footer.cgi %>
