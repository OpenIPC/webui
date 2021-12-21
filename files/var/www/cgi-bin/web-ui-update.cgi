#!/usr/bin/haserl
<%in _common.cgi %>
<%
url="https://github.com/OpenIPC/microbe-web/archive/refs/heads/${POST_version}.zip"
tmp_file=/tmp/microbe.zip
etag_file=/root/.ui.etag

opts="-skL --etag-save $etag_file"
if [ -z "$POST_enforce" ]; then
  opts="${opts} --etag-compare ${etag_file}"
fi

echo "$(date +"%F %T"): curl ${opts} -o ${tmp_file} ${url}" >> /tmp/webui-update.log
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
<%
else
  if [ -z "$POST_debug" ]; then
    redirect_to "/cgi-bin/progress.cgi"
  else
    http_header_text
    http_header_connection_close
    echo ""
  fi

  unzip -o -d /tmp $tmp_file > /dev/null

  upd_dir="/tmp/microbe-web-${POST_version}/files"
  # copy newer files to web directory
  for upd_file in $(find "${upd_dir}/var/www" -type f -or -type l); do
    www_file=${upd_file#/tmp/microbe-web-${POST_version}/files}
    if [ ! -f "$www_file" ] || [ ! -z "$(diff "$www_file" "$upd_file")" ]; then
      [ ! -d "${www_file%/*}" ] && mkdir -p "${www_file%/*}"
      cp -f "$upd_file" "$www_file"
    fi
  done

  # remove absent files from overlay
  for file in $(diff -qr "/var/www" "${upd_dir}/var/www" | grep "Only in /var/www:" | cut -d ":" -f 2 | tr -d "^ "); do
    if [ "$file" != "$etag_file" ]; then
      rm -vf "/var/www/${file}"
    fi
  done

  # clean up
  rm -f "${tmp_file}"
  rm -fr "/tmp/microbe-web-${POST_version}"

  echo "done."
fi
%>
