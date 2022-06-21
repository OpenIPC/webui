<div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasDebug" aria-labelledby="offcanvasDebugLabel">
  <div class="offcanvas-header">
    <h5 class="offcanvas-title" id="offcanvasLabel">Debug Info</h5>
    <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
  </div>
  <div class="offcanvas-body x-small">
    <% ex "printenv|grep REQUEST_|sort" %>
    <% ex "printenv|grep FORM_|sort" %>
    <% ex "printenv|grep GET_|sort" %>
    <% ex "printenv|grep POST_|sort" %>
    <% ex "cat /tmp/sysinfo.txt" %>
    <% ex "env|sort" %>
  </div>
</div>

<button class="btn btn-primary fixed-bottom" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasDebug" aria-controls="offcanvasDebug">Debug info</button>
