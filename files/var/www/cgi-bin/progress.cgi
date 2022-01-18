#!/usr/bin/haserl
<%in _common.cgi %>
<%
if [ -f /tmp/webjob.lock ]; then
  page_title="$tPageTitleProgress"
%>
<%in _header.cgi %>
<progress id="timer" max="20" value="0" class="w-100"></progress>
<script>
function tick() {
    tock += 1;
    $('#timer').value = tock;
    (tock === max) ? window.location.replace("/cgi-bin/progress.cgi") : setTimeout(tick, 1000);
}
function engage() {
    max = $('#timer').max;
    setTimeout(tick, 1000);
}
engage();
</script>
<%in _footer.cgi %>
<% else
redirect_to "/cgi-bin/firmware.cgi"
fi %>
