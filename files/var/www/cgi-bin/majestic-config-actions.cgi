#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title=$tMjMaintenance
%>
<%in _header.cgi %>
<div class="row row-cols-1 row-cols-xl-2 g-4 mb-3">
  <div class="col">
    <div class="card h-100">
      <div class="card-header"><%= $tMjBackupHeader %></div>
      <div class="card-body">
        <p><%= $tMjBackupInfo %></p>
        <a class="btn btn-primary" href="/cgi-bin/majestic-config-backup.cgi"><%= $tMjBackupButton %></a>
      </div>
    </div>
  </div>
  <div class="col">
    <div class="card h-100">
      <div class="card-header"><%= $tMjRestoreHeader %></div>
      <div class="card-body">
        <form action="/cgi-bin/majestic-config-restore.cgi" method="post" enctype="multipart/form-data">
          <div class="row mb-3">
            <p><%= $tMjRestoreInfo %></p>
            <label class="col-md-3 form-label" for="upfile"><%= $tMjBackupFile %></label>
            <div class="col-md-9">
              <input class="form-control" type="file" name="upfile" placeholder="majestic.yaml">
            </div>
          </div>
          <button type="submit" class="btn btn-danger"><%= $tMjRestoreButton %></button>
        </form>
      </div>
    </div>
  </div>
  <div class="col">
    <div class="card h-100">
      <div class="card-header"><%= $tMjChangesHeader %></div>
      <div class="card-body">
        <p><%= $tMjChangesInfo %></p>
        <a class="btn btn-primary" href="/cgi-bin/majestic-config-compare.cgi"><%= $tMjChangesButton %></a>
      </div>
    </div>
  </div>
  <div class="col">
    <div class="card h-100">
      <div class="card-header"><%= $tMjResetHeader %></div>
      <div class="card-body">
        <p><%= $tMjResetInfo %></p>
        <a class="btn btn-danger" href="/cgi-bin/majestic-config-reset.cgi"><%= $tMjResetButton %></a>
      </div>
    </div>
  </div>
</div>
<%in _footer.cgi %>
