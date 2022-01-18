#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleMajesticMaintenance"
%>
<%in _header.cgi %>
<div class="row row-cols-1 row-cols-xl-2 g-4 mb-3">
  <div class="col">
    <div class="card h-100">
      <div class="card-header"><%= $tHeaderMjBackup %></div>
      <div class="card-body">
        <p><%= $tMjBackupInfo %></p>
        <a class="btn btn-primary" href="/cgi-bin/majestic-config-backup.cgi"><%= $tButtonMjBackup %></a>
      </div>
    </div>
  </div>
  <div class="col">
    <div class="card h-100">
      <div class="card-header"><%= $tHeaderMjRestore %></div>
      <div class="card-body">
        <form action="/cgi-bin/majestic-config-restore.cgi" method="post" enctype="multipart/form-data">
          <div class="row mb-3">
            <p><%= $tMjRestoreInfo %></p>
            <label class="col-md-3 form-label" for="upfile"><%= $tMjBackupFile %></label>
            <div class="col-md-9">
              <input class="form-control" type="file" name="upfile" placeholder="majestic.yaml">
            </div>
          </div>
          <button type="submit" class="btn btn-danger"><%= $tButtonMjRestore %></button>
        </form>
      </div>
    </div>
  </div>
  <div class="col">
    <div class="card h-100">
      <div class="card-header"><%= $tHeaderMjChanges %></div>
      <div class="card-body">
        <p><%= $tMjChangesInfo %></p>
        <a class="btn btn-primary" href="/cgi-bin/majestic-config-compare.cgi"><%= $tButtonMjChanges %></a>
      </div>
    </div>
  </div>
  <div class="col">
    <div class="card h-100">
      <div class="card-header"><%= $tHeaderMjReset %></div>
      <div class="card-body">
        <p><%= $tMjResetInfo %></p>
        <a class="btn btn-danger" href="/cgi-bin/majestic-config-reset.cgi"><%= $tButtonMjReset %></a>
      </div>
    </div>
  </div>
</div>
<%in _footer.cgi %>
