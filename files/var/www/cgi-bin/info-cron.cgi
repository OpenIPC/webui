#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleCron"
%>
<%in _header.cgi %>
<b># cat /etc/crontabs/root</b>
<pre class="bg-light p-4 log-scroll">
<% cat /etc/crontabs/root %>
</pre>
<%in _footer.cgi %>
