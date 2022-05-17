#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleHttpdConfig"
%>
<%in _header.cgi %>
<b># cat /etc/httpd.conf</b>
<pre class="bg-light p-4 log-scroll">
<% cat /etc/httpd.conf %>
</pre>
<%in _footer.cgi %>
