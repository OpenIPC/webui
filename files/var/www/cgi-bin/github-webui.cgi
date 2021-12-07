#!/usr/bin/haserl
<%
command="curl --silent --head https://codeload.github.com/OpenIPC/microbe-web/zip/refs/heads/themactep-dev"
output=$($command 2>&1)
result=$?
if [ "0" -ne "$result" ]; then
  error="$output"
else
  gh_headers="$output"
  gh_etag=$(echo "$gh_headers" | grep "ETag:" | cut -d " " -f2 | sed 's/"//g')
  etag_file=/var/www/.etag
  etag=""
  [ -f "$etag_file" ] && etag=$(cat $etag_file)
  [ "$etag" = "$gh_etag" ] && error="It is the same version. Nothing to update."
fi

if [ ! -z "$error" ]; then %>
<%in _header.cgi %>
<h2 class="text-danger">Oops. Something happened.</h2>
<div class="alert alert-danger"><%= "$error" %></div>
<%in _footer.cgi %>
<% else
  command="curl --verbose --silent --insecure --location --output /tmp/microbe-dev.zip https://github.com/OpenIPC/microbe-web/archive/refs/heads/themactep-dev.zip"
  output=$($command 2>&1)
  result=$?
  if [ "0" -ne "$result" ]; then %>
<%in _header.cgi %>
<h2 class="text-danger">Oops. Something happened.</h2>
<div class="alert alert-danger">
<pre><%= "$output" %></pre>
</div>
<%in _footer.cgi %>
<% else
    echo "HTTP/1.1 302 Moved Temporarily"
    echo "Content-type: text/html; charset=UTF-8"
    echo "Date: $(TZ=GMT date +"%a, %d %b %Y %T %Z")"
    echo "Location: /cgi-bin/progress.cgi"
    echo "Server: httpd"
    echo "Status: 302 Moved Temporarily"
  fi

  unzip -o -d /tmp /tmp/microbe-dev.zip
  cp -av /tmp/microbe-web-themactep-dev/files/var/www /var/
  echo "$gh_etag" > "$etag_file"
  rm -rf /tmp/microbe-dev.zip /tmp/microbe-web-themactep-dev
fi
%>
