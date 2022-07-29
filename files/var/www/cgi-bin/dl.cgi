#!/usr/bin/haserl
<%in p/common.cgi %>
<%
filename=$GET_file
filepath=/tmp/webui/${filename}

[ ! -f "$filepath" ] && redirect_back "danger" "File ${filename} not found"

echo "HTTP/1.0 200 OK
Date: $(time_http)
Server: $SERVER_SOFTWARE
Content-type: text/plain
Content-Disposition: attachment; filename=${filename}
Content-Length: $(wc -c $filepath | cut -d' ' -f1)
Cache-Control: no-store
Pragma: no-cache
"
cat ${filepath}
%>
