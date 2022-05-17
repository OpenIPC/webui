#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleHttpdEnv"
%>
<%in _header.cgi %>
<b># printenv</b>
<pre class="bg-light p-4 log-scroll">
<% printenv | sort %>
</pre>
<%in _footer.cgi %>
