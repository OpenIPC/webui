#!/usr/bin/haserl
<% page_title="printenv" %>
<%in ../_common.cgi %>
<%in ../_header.cgi %>
<h2># printenv</h2>
<pre><% printenv | sort %></pre>
<%in ../_footer.cgi %>
