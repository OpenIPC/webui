#!/usr/bin/haserl
<%in p/common.cgi %>
<%
file=$GET_file
[ ! -f "$file" ] && redirect_back "danger" "File ${file} not found"
echo "HTTP/1.0 200 OK
Date: $(time_http)
Server: $SERVER_SOFTWARE
Content-type: application/octet-stream
Content-Disposition: attachment; filename=$(basename $file)
Content-Length: $(wc -c $file | cut -d' ' -f1)
Cache-Control: no-store
Pragma: no-cache
"
cat $file
%>
