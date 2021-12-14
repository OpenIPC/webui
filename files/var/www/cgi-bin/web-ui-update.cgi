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
<% else
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
  for upd_file in $(find "${upd_dir}/var/www" -type f); do
    file=${upd_file#/tmp/microbe-web-${POST_version}/files}
    if [ -z "$(diff -q "$upd_file" "/rom${file}")" ]; then
#      rm -vf "/overlay/root${file}"
      ln -sf "/rom${file}" "${file}"
    else
      if [ -n "$(diff -q "$upd_file" "$file")" ]; then
        [ ! -d "${file%/*}" ] && mkdir -p "${file%/*}"
        cp -f "$upd_file" "$file"
      fi
    fi
  done

  # remove absent files from overlay
  for file in $(diff -qr "/var/www" "${upd_dir}/var/www" | grep "Only in /var/www:" | cut -d ":" -f 2 | tr -d "^ "); do
    [ "$file" != "$wtag_file" ] && rm -vf "/var/www/${file}"
  done

  # clean up
  rm -vf "${tmp_file}"
  rm -vfr "/tmp/microbe-web-${POST_version}"
fi
%>
