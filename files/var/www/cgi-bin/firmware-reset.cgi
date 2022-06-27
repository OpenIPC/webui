#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="Erasing overlay" %>
<%in p/header.cgi %>
<pre class="bg-light p-4 log-scroll">
<% sysupgrade -n %>
</pre>
<a class="btn btn-primary" href="/">Go home</a>
<a class="btn btn-danger" href="/cgi-bin/reboot.cgi">Reboot camera</a>
<%in p/footer.cgi %>
