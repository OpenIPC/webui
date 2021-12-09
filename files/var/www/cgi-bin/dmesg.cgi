#!/usr/bin/haserl
<%in _header.cgi %>
<h2>Diagnostic message</h2>

<div class="row">
  <div class="col">
    <div class="card mb-3">
      <div class="card-header">dmesg</div>
      <div class="card-body">
        <pre><%= "$(dmesg)" %></pre>
        <a class="btn btn-primary" onClick="window.location.reload();">Refresh</a>
      </div>
    </div>
  </div>
</div>

<%in _footer.cgi %>
