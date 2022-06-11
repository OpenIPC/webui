<%
  _container
_main

footer_ "class=\"p-3\""
  container_
    div_ "class=\"float-start\""
      p "$(uname -a)" "class=\"mb-0\""
      p "${tPageGeneratedOn}&nbsp;$(date) ($(beats))" "class=\"text-muted\""
    _div

    p "${tPoweredBy} $(link_to "Microbe Web UI" "https://github.com/OpenIPC/microbe-web"), ${tPartOf} $(link_to "OpenIPC project" "https://openipc.org/")" "class=\"text-end\""
  _container
_footer
%>
</body>
</html>
