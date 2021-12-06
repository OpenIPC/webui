#!/usr/bin/haserl
content-type: text/html

<%in _header.cgi %>
<%
gh_headers=$(curl --silent --head https://codeload.github.com/OpenIPC/microbe-web/zip/refs/heads/themactep-dev)
gh_etag=$(echo "$gh_headers" | grep "ETag:" | cut -d " " -f2 | sed 's/"//g')
etag_file=/var/www/.etag
etag=""
[ -f "$etag_file" ] && etag=$(cat $etag_file)
if [ "$etag" = "$gh_etag" ]; then
%>
<h2>It is the same version. Nothing to update.</h2>
<% else %>
<h2>Downloading latest Web UI. Please wait...</h2>
<progress id="timer" max="90" value="0" class="w-100"></progress>
<script>window.onload = engage;</script>
<%
  debug_microbe
  echo "$gh_etag" > "$etag_file"
fi
%>
<%in _footer.cgi %>
