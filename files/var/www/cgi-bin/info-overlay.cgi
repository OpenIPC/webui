#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleOverlay"
%>
<%in _header.cgi %>
<b># ls -Rl /overlay</b>
<pre class="bg-light p-4">
<% ls -Rl /overlay %>
</pre>
<%in parts/reset-firmware.cgi %>
<%in _footer.cgi %>

