#!/usr/bin/haserl
<% page_title="logread" %>
<%in _common.cgi %>
<%in _header.cgi %>
<b># logread</b>
<pre class="bg-light p-4 log-scroll">
<%= "$(logread | tail -100)" %>
</pre>
<a class="btn btn-primary refresh"><%= $tButtonRefresh %></a>
<%in _footer.cgi %>
