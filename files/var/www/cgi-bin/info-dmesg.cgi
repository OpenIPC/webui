#!/usr/bin/haserl
<% page_title="dmesg" %>
<%in _common.cgi %>
<%in _header.cgi %>
<b># dmesg</b>
<pre class="bg-light p-4 log-scroll">
<%= "$(dmesg)" %>
</pre>
<a class="btn btn-primary refresh"><%= $tButtonRefresh %></a>
<%in _footer.cgi %>
