#!/usr/bin/haserl
<%in _common.cgi %>
<%
zipdir="microbe-web-${POST_version}"
url="https://github.com/OpenIPC/microbe-web/archive/refs/heads/${POST_version}.zip"
tmp_file=/tmp/microbe.zip
etag_file=/root/.ui.etag
opts="-skL --etag-save $etag_file"
[ -z "$POST_enforce" ] && opts="$opts --etag-compare $etag_file"

command="curl $opts -o $tmp_file $url"
output=$(curl $opts -o $tmp_file $url 2>&1)
result=$?
if [ "0" -ne "$result" ]; then
  error="$output"
elif [ ! -f "$tmp_file" ]; then
  error="GitHub version matches the installed one. Nothing to update."
fi

if [ ! -z "$error" ]; then %>
<%in _header.cgi %>
<% report_error "$error" %>
<%in _footer.cgi %>
<% else
    if [ -z "$POST_debug" ]; then
      redirect_to "/cgi-bin/progress.cgi"
    else
      http_header_html
    fi
  fi
  echo "$command"
  echo ""
  unzip -o -d /tmp ${tmp_file} 2>&1
  cp -au /tmp/${zipdir}/files/var/www /var/ 2>&1
  rm -rfv ${tmp_file} /tmp/${zipdir} 2>&1
  echo ${gh_etag} > ${etag_file}
fi
%>
