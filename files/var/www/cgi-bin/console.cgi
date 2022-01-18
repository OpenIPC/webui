#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleWebConsole"
cmd=$FORM_cmd
%>
<%in _header.cgi %>
<div class="console">
  <div class="input-group mb-3">
    <div class="input-group-text">~#</div>
    <input class="form-control" type="text" id="cmd" value="<%= $cmd %>"
      placeholder="<%= $tWebConsoleCmdPlaceholder %>" autofocus>
    <div class="input-group-text">
      <button type="button" class="btn btn-sm btn-white p-0" id="submit-cmd">⏎</button>
    </div>
  </div>
  <pre class="bg-light p-4 log-scroll" id="code">
  </pre>
</div>
<script>
jx = {
    handler: false,
    error: false,
    opt: new Object(),

    load: function (url, callback, format = "text", method = "GET") {
        const xhr = new XMLHttpRequest();
        method = method.toUpperCase();
        format = format.toLowerCase();

        url += (url.indexOf("?") + 1) ? "&" : "?";
        url += "uid=" + new Date().getTime();

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
function runCommand(cmd) {
    window.curcmd = cmd;
    jx.load('/cgi-bin/ajaxcmd.cgi?cmd=' + urlencode(cmd), handler, 'text', 'POST');
    return false;
}
function runCommandFromWeb(event) {
    if (event.keyCode && event.keyCode !== 13) return;
    const cmd = $('#cmd').value;
    return runCommand(cmd);
}
function urlencode(str) {
    return str.replace(/%/g, '%25').replace(/\+/g, '%2B')
        .replace(/%20/g, '+').replace(/\*/g, '%2A')
        .replace(/\//g, '%2F').replace(/@/g, '%40')
        .replace(/&/g, '%26').replace(/;/g, '%3B')
        .replace(/\$/g, '%24').replace(/\?/g, '%3F');
}
window.addEventListener('load', () => {
  $('#cmd').addEventListener('keyup', runCommandFromWeb);
  $('#submit-cmd').addEventListener('click', (event) => {
    runCommandFromWeb(event);
    $('#cmd').focus();
    event.preventDefault();
  });
});
</script>

<%in _footer.cgi %>
