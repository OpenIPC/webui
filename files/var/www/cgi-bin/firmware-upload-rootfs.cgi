#!/usr/bin/haserl --upload-limit=5120 --upload-dir=/tmp
<%in _common.cgi %>
<%in _header.cgi %>
<%
maxsize=5242880
magicnum="68737173"

sysupgrade_date=$(ls -lc --full-time /usr/sbin/sysupgrade | xargs | cut -d " " -f 6)
sysupgrade_date=$(date --date="$sysupgrade_date" +"%s")
new_sysupgrade_date=$(date --date="2022-02-22" +"%s")

file="$POST_rootfs_file"
name="$POST_rootfs_file_name"

error=""
if [ -z "$name"  ]; then
  error="No file found! Did you forget to upload?"
elif [ ! -r "$file" ]; then
  error="Cannot read file \"${name}\" from \"${file}\"!"
elif [ "$(wc -c "$file" | awk '{print $1}')" -gt "$maxsize" ]; then
  error="File \"${name}\" is too large! Its size is $(wc -c "$file" | awk '{print $1}') bytes, but it should be ${maxsize} bytes or less."
elif [ "$magicnum" -ne "$(xxd -p -l 4 "$file")" ]; then
  error="File magic number does not match. Did you upload a wrong file? $(xxd -p -l 4 "$file") != $magicnum"
elif [ "$sysupgrade_date" -lt "$new_sysupgrade_date" ]; then
  error="This feature requires the latest sysupgrade tool. Please upgrade firmware first."
fi

if [ ! -z "$error" ]; then
  report_error "$error"
else
  pre_ "class=\"bg-light p-4 log-scroll\""
  mv ${file} /tmp/${name}
  sysupgrade --rootfs=/tmp/${name} --force_ver --force_all
  _pre
  button_home
fi
%>
<%in _footer.cgi %>
