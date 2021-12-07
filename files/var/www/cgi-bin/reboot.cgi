#!/usr/bin/haserl
<%in _header.cgi %>
<h2>Trying to reboot. Please wait...</h2>
<progress id="timer" max="60" value="0" class="w-100"></progress>
<script>window.onload = engage;</script>
<%in _footer.cgi %>
<% reboot -d 3 %>
