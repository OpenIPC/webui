    </div>
  </main>

  <footer class="x-small">
    <div class="container pt-3">
      <p class="text-end">Powered by <a href="https://github.com/OpenIPC/microbe-web">Microbe Web UI</a>, a part of <a href="https://openipc.org/">OpenIPC project</a>.</p>
    </div>
  </footer>

<% if [ "$debug" -ge "1" ]; then %>
  <button id="debug-button" type="button" class="btn btn-primary btn-sm m-2 float-start"
    data-bs-toggle="offcanvas" data-bs-target="#offcanvasDebug"
    aria-controls="offcanvasDebug">Debug</button>
  <div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasDebug" aria-labelledby="offcanvasDebugLabel">
    <div class="offcanvas-header">
      <h5 class="offcanvas-title" id="offcanvasDebugLabel">Debug Info</h5>
      <form action="webui.cgi" method="post">
        <% field_hidden "action" "init" %>
        <% button_submit "Refresh Environment" %>
      </form>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body x-small">
      <ul class="nav nav-tabs" role="tablist">
        <% tab_lap "t1" "sysinfo" "active" %>
        <% tab_lap "t2" "env" %>
      </ul>
      <div class="tab-content p-2" id="tab-content">
        <div id="t1-tab-pane" role="tabpanel" class="tab-pane fade active show" aria-labelledby="t1-tab" tabindex="0">
          <% ex "cat /tmp/sysinfo.txt" %>
        </div>
        <div id="t2-tab-pane" role="tabpanel" class="tab-pane fade" aria-labelledby="t2-tab" tabindex="0">
          <% ex "env | sort" %>
        </div>
      </div>
    </div>
  </div>
<% fi %>
</body>
</html>
