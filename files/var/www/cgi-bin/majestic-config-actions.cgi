#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="$t_mjactions_0" %>
<%in p/header.cgi %>
<div class="row row-cols-1 row-cols-lg-2 row-cols-xxl-4 g-4">
<div class="col">
<h3><%= $t_mjactions_1 %></h3>
<p><%= $t_mjactions_2 %></p>
<a class="btn btn-primary" href="/cgi-bin/majestic-config-backup.cgi"><%= $t_mjactions_3 %></a>
</div>
<div class="col">
<h3><%= $t_mjactions_4 %></h3>
<p><%= $t_mjactions_5 %></p>
<form action="/cgi-bin/majestic-config-restore.cgi" method="post" enctype="multipart/form-data">
<%
field_file "mj_restore_file"
button_submit "$t_mjactions_7"
%>
</form>
</div>
<div class="col">
<h3><%= $t_mjactions_8 %></h3>
<p><%= $t_mjactions_9 %></p>
<a class="btn btn-primary" href="/cgi-bin/majestic-config-compare.cgi"><%= $t_mjactions_a %></a>
</div>
<div class="col">
<h3><%= $t_mjactions_b %></h3>
<p><%= $t_mjactions_c %></p>
<a class="btn btn-danger" href="/cgi-bin/majestic-config-reset.cgi"><%= $t_mjactions_d %></a>
</div>
</div>
<%in p/footer.cgi %>
