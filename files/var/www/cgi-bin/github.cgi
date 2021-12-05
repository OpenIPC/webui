#!/usr/bin/haserl
content-type: text/html

<%in _header.cgi %>
<h2>Downloading firmware. Please wait...</h2>
<progress id="timer" max="120" value="0" class="w-100"></progress>
<script>window.onload = engage;</script>
<%in _footer.cgi %>
<% [ -z "$FORM_reset" ] && (sysupgrade > /dev/null) || (sysupgrade -n > /dev/null) %>
