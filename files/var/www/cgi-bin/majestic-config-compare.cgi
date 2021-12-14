#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="Majestic Changes"
command="diff /rom/etc/majestic.yaml /etc/majestic.yaml"
output=$($command 2>&1)
result=$?
%>
<%in _header.cgi %>
<h2>Changes in Majestic config</h2>
<% flash_read %>
<%
# diff returns 0 on no difference, 1 on difference, 2+ on errors
# checking exit status won't work here
# checking for any output instead
if [ -z "$output" ]; then %>
<% report_info "No changes found." %>
<% else %>
<% report_command_info "$command" "$output" %>
<% fi %>
<p class="d-flex gap-2">
  <a class="btn btn-secondary" href="/cgi-bin/majestic-config-backup.cgi">Download config</a>
  <a class="btn btn-danger" href="/cgi-bin/majestic-config-reset.cgi">Restore original</a>
</p>
<%in _footer.cgi %>
