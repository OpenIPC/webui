#!/usr/bin/haserl
<%in p/common.cgi %>
<%
filepath=/tmp/webui.log
[ ! -f "$filepath" ] && redirect_back "danger" "File ${filepath} not found"

echo "HTTP/1.0 200 OK
Date: $(time_http)
Server: $SERVER_SOFTWARE
Content-type: text/plain
Content-Disposition: attachment; filename=webui-$(date +%s).log
Content-Length: $(wc -c $filepath | cut -d' ' -f1)
Cache-Control: no-store
Pragma: no-cache
"
cat ${filepath}
%>
