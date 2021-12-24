#!/usr/bin/haserl
<%in _common.cgi %>
<%
url="https://github.com/OpenIPC/microbe-web/archive/refs/heads/${POST_version}.zip"
tmp_file=/tmp/microbe.zip
etag_file=/root/.ui.etag

opts="-skL --etag-save $etag_file"
[ -z "$POST_enforce" ] && opts="${opts} --etag-compare ${etag_file}"

echo "$(date +"%F %T"): curl ${opts} -o ${tmp_file} ${url}" >> /tmp/webui-update.log
output=$(curl $opts -o $tmp_file $url 2>&1)
if [ 0 -ne $? ]; then
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
  else %>
<%in _debug.cgi %>
<% fi
  commit=$(tail -c 40 $tmp_file | cut -b1-7)
  timestamp=$(unzip -l $tmp_file | head -5 | tail -1 | xargs | cut -d" " -f2 | sed 's/\(\d\d\)-\(\d\d\)-\(\d\d\d\d\)/\3-\1-\2/')

  unzip_dir="/tmp/microbe-web-${POST_version}"
  [ -d "$unzip_dir" ] && rm -rf ${unzip_dir} 2>&1
  unzip -o -d /tmp $tmp_file -x microbe-web-dev/README.md microbe-web-dev/.git* microbe-web-dev/LICENSE microbe-web-dev/docs/* microbe-web-dev/wirebox/* 2>&1

  upd_dir="${unzip_dir}/files"
  # copy newer files to web directory
  for upd_file in $(find "${upd_dir}/var/www" -type f -or -type l); do
    www_file=${upd_file#/tmp/microbe-web-${POST_version}/files}
    diff ${www_file} ${upd_file} > /dev/null
    if [ 0 -ne $? ]; then
      [ ! -d "${www_file%/*}" ] && mkdir -p "${www_file%/*}" 2>&1
      echo "cp -f ${upd_file} ${www_file}"
      cp -f ${upd_file} ${www_file} 2>&1
    fi
  done

  # remove absent files from overlay
  for file in $(diff -qr "/var/www" "${upd_dir}/var/www" | grep "Only in /var/www:" | cut -d ":" -f 2 | tr -d "^ "); do
    if [ "$file" != "$etag_file" ]; then
      echo "rm -f /var/www/${file}"
      rm -f "/var/www/${file}" 2>&1
    fi
  done

  # clean up
  echo "rm -f ${tmp_file}"
  rm -f ${tmp_file} 2>&1
  echo "rm -fr /tmp/microbe-web-${POST_version}"
  rm -fr /tmp/microbe-web-${POST_version} 2>&1

  echo "echo \"${POST_version}+${commit}, ${timestamp}\" > /var/www/.version"
  echo "${POST_version}+${commit}, ${timestamp}" > /var/www/.version

  echo "done."
fi
%>
