#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="Log read" %>
<%in p/header.cgi %>
<% ex "/sbin/logread" %>
<% button_refresh %>
<% button_download "logread" %>

<% if [ -z "$(eval echo "DEBUG TRACE" | sed -n "/\b$(yaml-cli -g .system.logLevel)\b/p")" ]; then %>
<div class="alert alert-warning my-3">
<p><a class="btn btn-warning disabled">Send Majectic log to PasteBin</a></p>
<p class="mb-0">Please enable DEBUG level of logging <a href="majestic-settings.cgi?tab=system">in Majectic config</a> to activate the button.</p>
</div>
<% else %>
<a class="btn btn-warning" href="send.cgi?to=pastebin&file=mjlog" target="_blank">Send Majectic log to PasteBin</a>
<% fi %>

<%in p/footer.cgi %>
