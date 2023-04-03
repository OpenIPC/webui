#!/usr/bin/haserl --upload-limit=5120 --upload-dir=/tmp
<%in p/common.cgi %>
<%
sysupgrade_date=$(ls -lc --full-time /usr/sbin/sysupgrade | xargs | cut -d' ' -f6)
sysupgrade_date=$(time_epoch "$sysupgrade_date")

file="$POST_parts_file"
file_name="$POST_parts_file_name"
error=""

case "$POST_parts_type" in
kernel)
  maxsize=2097152
  magicnum="27051956"
  new_sysupgrade_date=$(time_epoch "2021-12-07")
  cmd="sysupgrade --kernel=/tmp/${file_name} --force_ver"
  ;;
rootfs)
  maxsize=5242880
  magicnum="68737173"
  new_sysupgrade_date=$(time_epoch "2022-02-22")
  cmd="sysupgrade --rootfs=/tmp/${file_name} --force_ver --force_all"
  ;;
*)
  error="Please select type of file and upload it again!"
  ;;
esac

[ -z "$file_name"  ] && error="No file found! Did you forget to upload?"
[ ! -r "$file" ] && error="Cannot read uploded file!"
[ "$(stat -c%s $file)" -gt "$maxsize" ] && error="Uploded file is too large! $(stat -c%s $file) > ${maxsize}."
[ "$magicnum" -ne "$(xxd -p -l 4 $file)" ] && error="File magic number does not match. Did you upload a wrong file? $(xxd -p -l 4 $file) != $magicnum"
[ "$sysupgrade_date" -lt "$new_sysupgrade_date" ] && error="This feature requires the latest sysupgrade tool. Please upgrade firmware first."

if [ -n "$error" ]; then
  redirect_back "danger" "$error"
else %>
<%in p/header.cgi %>
<pre class="bg-light p-4 log-scroll">
<%
xl "mv $file /tmp/${file_name}"
$cmd
%>
</pre>
<a class="btn btn-primary" href="/">Go home</a>
<% fi %>
<%in p/footer.cgi %>
