#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Web console"
cmd="$FORM_cmd"
%>
<%in p/header.cgi %>

<div class="console">
  <div class="input-group mb-3">
    <div class="input-group-text">/tmp#</div>
    <input class="form-control" type="text" id="cmd" value="<%= $cmd %>" placeholder="Type a command and hit Enter" required autofocus>
    <div class="input-group-text p-0"><button type="button" class="btn btn-sm btn-white" id="submit-cmd">⏎</button></div>
  </div>
  <pre class="log-scroll" id="code"></pre>
</div>

<script>
jx = {
  handler: false, error: false, opt: new Object(),
  load: function (url, callback, format = "text", method = "GET") {
    const xhr = new XMLHttpRequest();
    method = method.toUpperCase();
    format = format.toLowerCase();
    url += ((url.indexOf("?") + 1) ? "&" : "?") + "uid=" + new Date().getTime();
    let parameters = null;
    if (method === "POST") {
      const parts = url.split("?");
      url = parts[0];
      parameters = parts[1];
    }
    xhr.open(method, url, true);
    if (method === "POST") xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          let result = "";
          switch (xhr.responseType) {
            case "json":
              result = eval("(" + xhr.responseText.replace(/[\n\r]/g, "") + ")");
              break;
            case "xml":
              result = xhr.responseXML;
              break;
            default:
              result = xhr.responseText;
          }
          callback(result);
        } else {
          if (xhr.error) xhr.error(xhr.status);
        }
      }
    }
    xhr.send(parameters);
  }
}

function handler(data) {
  $("#code").innerHTML = data;
}

function runCommand() {
  cmd = $("#cmd").value.trim();
  if (cmd.length == 0) return;
  jx.load("/cgi-bin/j/run.cgi?cmd=" + btoa(cmd), handler, "text", "GET");
  return false;
}

window.addEventListener("load", () => {
  $("#cmd").addEventListener("keyup", (ev) => {
    if (ev.keyCode && ev.keyCode == 13)
      runCommand();
  });

  $("#submit-cmd").addEventListener("click", (ev) => {
    runCommand();
    $("#cmd").focus();
    ev.preventDefault();
  });
});
</script>
<%in p/footer.cgi %>
