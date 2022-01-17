</div>
</main>
<footer class="p-3">
<div class="container">
<div class="float-start">
<p class="mb-1"><%= $(uname -a) %></p>
<p class="text-muted"><%= $tPageGeneratedOn %>&nbsp;<%= $(date) %> (<% beats %>)</p>
</div>
<p class="text-end"><%= $tPoweredBy %> <a href="https://github.com/OpenIPC/microbe-web">Microbe Web UI</a>,
  <%= $tPartOf %> <a href="https://openipc.org/">OpenIPC project</a>.</p>
</div>
</footer>
</body>
</html>
