#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_system_info
page_title="$tPageTitlePreviewMjpeg"
size=$(yaml-cli -g .mjpeg.size)
[ -z "$size" ] && size="640x480"
size_w=${size%x*}; size_h=${size#*x} %>
<%in _header.cgi %>
<div class="row preview">
<div class="col mb-4">
<img class="img-fluid" id="preview" width="<%= $size_w %>" height="<%= $size_h %>" alt="MJPEG Preview">
</div>
</div>
<%in _joystick.cgi %>
<script>
// Based on https://github.com/aruntj/mjpeg-readable-stream
const CONTENT_LENGTH = 'content-length';
const TYPE_JPEG = 'image/jpeg';
const SOI = new Uint8Array(2);
const mjpeg_url = "http://<%= $ipaddr %>/mjpeg";
SOI[0] = 0xFF;
SOI[1] = 0xD8;
let image = $('#preview');
fetch(mjpeg_url).then(response => {
  if (!response.ok) throw Error(response.status + ' ' + response.statusText);
  if (!response.body) throw Error('ReadableStream not yet supported in this browser.');
  const reader = response.body.getReader();
  let headers = '';
  let contentLength = -1;
  let imageBuffer = null;
  let bytesRead = 0;
  const read = () => {
    reader.read().then(({done, value}) => {
      if (done) {
        controller.close();
        return;
      }
      for (let index = 0; index < value.length; index++) {
        if (value[index] === SOI[0] && value[index + 1] === SOI[1]) {
          contentLength = getLength(headers);
          imageBuffer = new Uint8Array(new ArrayBuffer(contentLength));
        }
        if (contentLength <= 0) {
          headers += String.fromCharCode(value[index]);
        } else if (bytesRead < contentLength) {
          imageBuffer[bytesRead++] = value[index];
        } else {
          let frame = URL.createObjectURL(new Blob([imageBuffer], {type: TYPE_JPEG})); //'video/x-motion-jpeg'
          image.src = frame;
          image.onload = function() {
            URL.revokeObjectURL(frame);
            contentLength = 0;
            bytesRead = 0;
            headers = '';
          }
        }
      }
      read();
    }).catch(error => {
      console.error(error);
    })
  }
  read();
}).catch(error => {
  console.error(error);
})
const getLength = (headers) => {
  let contentLength = -1;
  headers.split('\n').forEach((header, _) => {
    const pair = header.split(':');
    if (pair[0].toLowerCase() === CONTENT_LENGTH) contentLength = pair[1];
  })
  return contentLength;
};
</script>
<%in _footer.cgi %>
