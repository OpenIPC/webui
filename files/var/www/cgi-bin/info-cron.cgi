#!/usr/bin/haserl
<% page_title="cron" %>
<%in _common.cgi %>
<%in _header.cgi %>
<b># cat /etc/crontabs/root</b>
<pre class="bg-light p-4"><% cat /etc/crontabs/root %></pre>
<%in _footer.cgi %>
