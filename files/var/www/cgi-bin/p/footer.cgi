</div>
</main>
<footer class="x-small p-3">
<div class="container p-3">
<p class="text-end"><%= $tPoweredBy %> <a href="https://github.com/OpenIPC/microbe-web">Microbe Web UI</a>, <%= $tPartOf %> <a href="https://openipc.org/">OpenIPC project</a></p>
</div>
</footer>
<% if [ "development" = "$HTTP_MODE" ]; then %>
<%in p/debug-info.cgi %>      
<% fi %>
</body>
</html>
