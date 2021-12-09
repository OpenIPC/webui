#!/usr/bin/haserl
<%in _header.cgi %>
<h2>Log read</h2>

<div class="row">
  <div class="col">
    <div class="card mb-3">
      <div class="card-header">logread</div>
      <div class="card-body">
        <pre><%= "$(logread)" %></pre>
        <a class="btn btn-primary" onClick="window.location.reload();">Refresh</a>
      </div>
    </div>
  </div>
</div>

<%in _footer.cgi %>
