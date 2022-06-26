#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="$t_mjcompare_0" %>
<%in p/header.cgi %>

<div class="row">
  <div class="col-md-8 col-lg-9 col-xl-9 col-xxl-10">
<%
diff /rom/etc/majestic.yaml /etc/majestic.yaml > /tmp/majestic.patch
ex "cat /tmp/majestic.patch"
%>
  </div>
  <div class="col-md-4 col-lg-3 col-xl-3 col-xxl-2">
    <div class="d-grid d-sm-flex d-md-grid gap-2">
      <a class="btn btn-secondary" href="/cgi-bin/majestic-config-backup.cgi"><%= $t_mjcompare_2 %></a>
      <a class="btn btn-secondary" href="/cgi-bin/majestic-config-aspatch.cgi"><%= $t_mjcompare_3 %></a>
      <a class="btn btn-danger" href="/cgi-bin/majestic-config-reset.cgi"><%= $t_mjcompare_4 %></a>
    </div>
  </div>
</div>

<%in p/footer.cgi %>
