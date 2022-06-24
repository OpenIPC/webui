<% if [ "$debug" ]; then %>
<div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasDebug" aria-labelledby="offcanvasDebugLabel">
<div class="offcanvas-header">
<h5 class="offcanvas-title" id="offcanvasLabel">Debug Info</h5>
<button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
</div>
<div class="offcanvas-body x-small">
<p><a class="btn btn-warning" href="webui-init.cgi">Refresh Environment</a></p>
<% ex env %>
<% ex "cat /tmp/sysinfo.txt" %>
</div>
</div>
<button type="button" class="btn btn-primary fixed-bottom" data-bs-toggle="offcanvas" data-bs-target="#offcanvasDebug" aria-controls="offcanvasDebug">Debug</button>
<style>
:root{--bs-blue: #990000}
.offcanvas{--bs-offcanvas-width: 30vw}
</style>
<% fi %>
