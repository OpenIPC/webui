#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitlePreview"
%>
<%in _header.cgi %>
<div class="row preview">
  <div class="col position-relative mb-4">
    <img id="preview" src="http://<%= $ipaddr %>/image.jpg" class="img-fluid" width="1280" height="720" alt="">
  </div>
</div>
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
