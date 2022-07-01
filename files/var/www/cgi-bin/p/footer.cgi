    </div>
  </main>

  <footer class="fixed-bottom bg-light x-small">
    <div class="container pt-3">
      <p class="text-end">Powered by <a href="https://github.com/OpenIPC/microbe-web">Microbe Web UI</a>, a part of <a href="https://openipc.org/">OpenIPC project</a>.</p>
    </div>
  </footer>

<% if [ "$debug" -ge "1" ]; then %>
  <div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasDebug" aria-labelledby="offcanvasDebugLabel">
    <div class="offcanvas-header">
      <h5 class="offcanvas-title" id="offcanvasDebugLabel">Debug Info</h5>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body x-small">
      <form action="webui.cgi" method="post">
        <% field_hidden "action" "init" %>
        <% button_submit "Refresh Environment" %>
      </form>

      <ul class="nav nav-tabs" role="tablist">
        <% tab_lap "t1" "sysinfo" "active" %>
        <% tab_lap "t2" "env" %>
      </ul>
      <div class="tab-content p-2" id="tab-content">
        <div id="t1-tab-pane" role="tabpanel" class="tab-pane fade active show" aria-labelledby="t1-tab" tabindex="0">
          <% ex "env | sort" %>
        </div>
        <div id="t2-tab-pane" role="tabpanel" class="tab-pane fade" aria-labelledby="t2-tab" tabindex="0">
          <% ex "cat /tmp/sysinfo.txt" %>
        </div>
      </div>
    </div>
  </div>

  <button type="button" class="btn btn-primary btn-sm fixed-bottom m-2" data-bs-toggle="offcanvas" data-bs-target="#offcanvasDebug" aria-controls="offcanvasDebug">Debug</button>
<% fi %>
</body>
</html>
