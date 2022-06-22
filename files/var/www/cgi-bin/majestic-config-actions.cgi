#!/usr/bin/haserl
<%in _common.cgi %>
<% page_title="$t_mjactions_0" %>
<%in _header.cgi %>
<div class="row row-cols-1 row-cols-lg-2 row-cols-xxl-4 g-3 mb-3">
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_mjactions_1 %></div>
<div class="card-body">
<p><%= $t_mjactions_2 %></p>
<a class="btn btn-primary" href="/cgi-bin/majestic-config-backup.cgi"><%= $t_mjactions_3 %></a>
</div>
</div>
</div>
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_mjactions_4 %></div>
<div class="card-body">
<p><%= $t_mjactions_5 %></p>
<form action="/cgi-bin/majestic-config-restore.cgi" method="post" enctype="multipart/form-data" autocomplete="off">
<div class="mb-2 file">
<label class="form-label" for="mj_restore_file"><%= $t_mjactions_6 %></label>
<input type="file" name="mj_restore_file" id="mj_restore_file" class="form-control form-control" placeholder="majestic.yaml" value="">
</div>
<button type=submit class="btn btn-danger mt-3"><%= $t_mjactions_7 %></button>
</form>
</div>
</div>
</div>
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_mjactions_8 %></div>
<div class="card-body">
<p><%= $t_mjactions_9 %></p>
<a class="btn btn-primary" href="/cgi-bin/majestic-config-compare.cgi"><%= $t_mjactions_a %></a>
</div>
</div>
</div>
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_mjactions_b %></div>
<div class="card-body">
<p><%= $t_mjactions_c %></p>
<a class="btn btn-danger" href="/cgi-bin/majestic-config-reset.cgi"><%= $t_mjactions_d %></a>
</div>
</div>
</div>
</div>
<%in p/footer.cgi %>
