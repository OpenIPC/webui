#!/usr/bin/haserl
<% page_title="printenv" %>
<%in _common.cgi %>
<%in _header.cgi %>
<b># printenv</b>
<pre class="bg-light p-4"><% printenv | sort %></pre>
<%in _footer.cgi %>
