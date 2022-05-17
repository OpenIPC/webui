#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleDmesg"
%>
<%in _header.cgi %>
<b># dmesg</b>
<pre class="bg-light p-4 log-scroll">
<%= "$(dmesg)" %>
</pre>
<a class="btn btn-primary refresh"><%= $tButtonRefresh %></a>
<%in _footer.cgi %>
