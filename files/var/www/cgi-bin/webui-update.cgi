#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPT_WebuiUpdate"

ver="$POST_web_version"
url="https://github.com/OpenIPC/microbe-web/archive/refs/heads/${ver}.zip"
tmp_file=/tmp/microbe.zip
etag_file=/root/.ui.etag

opts="-skL --etag-save ${etag_file}"
[ -z "$POST_web_enforce" -a -f "$etag_file" ] && opts="${opts} --etag-compare ${etag_file}"
%>
<%in _header.cgi %>
<pre class="log-scroll">
<%
xl "curl ${opts} -o ${tmp_file} ${url}"
[ ! -f "$tmp_file" ] && echo "$tMsgSameVersion" && error=1

commit=$(tail -c 40 $tmp_file|cut -b1-7)
timestamp=$(unzip -l $tmp_file|head -5|tail -1|xargs|cut -d" " -f2|sed 's/\(\d\d\)-\(\d\d\)-\(\d\d\d\d\)/\3-\1-\2/')

unzip_dir="/tmp/microbe-web-${ver}"
[ -d "$unzip_dir" ] && xl "rm -rf $unzip_dir"

xl "unzip -o -d /tmp ${tmp_file} -x microbe-web-dev/README.md microbe-web-dev/.git* microbe-web-dev/LICENSE microbe-web-dev/docs/* microbe-web-dev/wirebox/*"

upd_dir="${unzip_dir}/files"
# copy newer files to web directory
for upd_file in $(find $upd_dir -type f -or -type l); do
  ovl_file=${upd_file#/tmp/microbe-web-${ver}/files}
  diff $ovl_file $upd_file > /dev/null
  if [ 0 -ne $? ]; then
    [ ! -d "${ovl_file%/*}" ] && xl "mkdir -p ${ovl_file%/*}"
    xl "cp -f ${upd_file} ${ovl_file}"
  fi
done

# remove absent files from overlay
for file in $(diff -qr "/var/www" "${upd_dir}/var/www" | grep "Only in /var/www:" | cut -d':' -f2 | tr -d "^ "); do
  [ "$file" != "$etag_file" ] && xl "rm -f /var/www/${file}"
done

# clean up
xl "rm -f ${tmp_file}"
xl "rm -fr /tmp/microbe-web-${ver}"

if [ -z "$error" ]; then
  xl "echo \"${ver}+${commit}, ${timestamp}\" > /var/www/.version"
else
  xl "rm $etag_file"
  echo "$tMsgAttentionErrors"
fi
%>
</pre>
<% button_home %>
<%in p/footer.cgi %>
