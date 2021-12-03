#!/usr/bin/haserl
content-type: text/html

<%in _header.cgi %>
<h2>Downloading firmware. Please wait...</h2>
<progress id="timer" max="120" value="0" class="w-100"></progress>
<script>
let tock = 0;
const max=$('#timer').max;
function tick() {
  tock += 1;
  $('#timer').value = tock;
  (tock == max) ? window.location.replace("/") : setTimeout(tick, 1000);
}
window.onload = setTimeout(tick, 1000);
</script>
<%in _footer.cgi %>
<% [ -z "$FORM_reset" ] && (sysupgrade > /dev/null) || (sysupgrade -n > /dev/null) %>
