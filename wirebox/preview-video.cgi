<div class="ratio ratio-16x9">
  <video id="preview-video" preload="metadata" poster="/a/SMPTE_Color_Bars_16x9.svg">
    <!-- source src="http://<%= $network_address %>/video.mp4" type="video/mp4" -->
    Your browser does not support HTML5 video.
  </video>
</div>

<script>
  let source = document.createElement('source');
  source.src = 'http://<%= $network_address %>/video.mp4?t='+Date.now();
  source.type = 'video/mp4';
  $('#preview-video').appendChild(source);
  $('#preview-video').play();

//  $('#preview-video').pause();
//  $('#preview-video source').remove();
</script>
