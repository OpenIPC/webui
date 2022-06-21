#!/usr/bin/haserl --upload-limit=5120 --upload-dir=/tmp
<%in _common.cgi %>
<%in _header.cgi %>
<%
maxsize=5242880
magicnum="68737173"

sysupgrade_date=$(ls -lc --full-time /usr/sbin/sysupgrade | xargs | cut -d' ' -f6)
sysupgrade_date=$(date +"%s" --date="$sysupgrade_date")
new_sysupgrade_date=$(date +"%s" --date="2022-02-22")

file="$POST_rootfs_file"
file_name="$POST_rootfs_file_name"

error=""
if [ -z "$file_name"  ]; then
  error="$t_form_error_1"
elif [ ! -r "$file" ]; then
  error="$t_form_error_2"
elif [ "$(wc -c $file | awk '{print $1}')" -gt "$maxsize" ]; then
  error="$t_form_error_3 $(wc -c $file | awk '{print $1}') > ${maxsize}."
elif [ "$magicnum" -ne "$(xxd -p -l 4 $file)" ]; then
  error="$t_form_error_4 $(xxd -p -l 4 $file) != $magicnum"
elif [ "$sysupgrade_date" -lt "$new_sysupgrade_date" ]; then
  error="$t_form_error_5"
fi

if [ -n "$error" ]; then
  report_error "$error"
else
  pre_ "bg-light p-4 log-scroll"
    xl "mv $file /tmp/${file_name}"
    sysupgrade --rootfs=/tmp/${file_name} --force_ver --force_all
  _pre
  button_home
fi
%>
<%in p/footer.cgi %>
