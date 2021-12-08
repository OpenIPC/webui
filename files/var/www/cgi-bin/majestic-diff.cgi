#!/usr/bin/haserl
<%in _common.cgi %>
<%
command="diff /rom/etc/majestic.yaml /etc/majestic.yaml"
output=$($command 2>&1)
result=$?
%>
<%in _header.cgi %>
<h2>Changes in Majestic config</h2>
<div class="row">
<div class="col-xl-8 mb-3">
<%
# diff returns 0 on no difference, 1 on difference, 2+ on errors
# checking exit status won't work here
# checking for any output instead
if [ -z "$output" ]; then %>
<% report_info "No changes found." %>
<% else %>
<% report_command_info "$command" "$output" %>
<% fi %>
</div>
<div class="col-xl-4 mb-3">
<p class="d-grid gap-2">
  <a class="btn btn-primary" href="/cgi-bin/majestic.cgi">Go to Majestic settings page</a>
  <a class="btn btn-danger" href="/cgi-bin/majestic-reset.cgi">Restore original configuration</a>
  <a class="btn btn-secondary" href="/cgi-bin/majestic-download.cgi">Download configuration file</a>
</p>
</div>
</div>
<%in _footer.cgi %>
