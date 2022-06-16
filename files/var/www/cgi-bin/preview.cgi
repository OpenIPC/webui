#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitlePreview"
%>
<%in _header.cgi %>
<%
row_ "preview"
  col_ "position-relative mb-4"
    image "http://${ipaddr}/image.jpg" "id=\"preview\" class=\"img-fluid\" width=\"1280\" height=\"720\""
  _col
_row
%>
<%in _joystick.cgi %>

<script>
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function updatePreview() {
  await sleep(1000);
  $('#preview').src = "http://<%= $ipaddr %>/image.jpg?t=" + Date.now();
}

function initPage() {
  $('#preview').addEventListener('load', updatePreview);
  updatePreview();
}

window.addEventListener('load', initPage);
</script>
<%in _footer.cgi %>
