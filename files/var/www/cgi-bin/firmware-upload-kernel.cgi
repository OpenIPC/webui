#!/usr/bin/haserl --upload-limit=2048 --upload-dir=/tmp
<%in _common.cgi %>
<%in _header.cgi %>
<%
maxsize=2097152
magicnum="27051956"

sysupgrade_date=$(ls -lc --full-time /usr/sbin/sysupgrade | xargs | cut -d' ' -f6)
sysupgrade_date=$(date +"%s" --date="$sysupgrade_date")
new_sysupgrade_date=$(date +"%s" --date="2021-12-07")

file=$POST_kernel_file
file_name=$POST_kernel_file_name

error=""
if [ -z "$file_name"  ]; then
  error="$tMsgNoUploadedFileFound"
elif [ ! -r "$file" ]; then
  error="$tMsgCannotReadUploadedFile"
elif [ "$(wc -c $file | awk '{print $1}')" -gt "$maxsize" ]; then
  error="$tMsgUploadedFileIsTooLarge $(wc -c $file | awk '{print $1}') > ${maxsize}."
elif [ "$magicnum" -ne "$(xxd -p -l 4 $file)" ]; then
  error="$tMsgUploadedFileHasWrongMagic $(xxd -p -l 4 $file) != $magicnum"
elif [ "$sysupgrade_date" -lt "$new_sysupgrade_date" ]; then
  error="This feature requires the latest sysupgrade tool. Please upgrade firmware first."
fi

if [ -n "$error" ]; then
  report_error "$error"
else
  pre_ "class=\"bg-light p-4 log-scroll\""
    mv $file /tmp/${file_name}
    sysupgrade --kernel=/tmp/${file_name} --force_ver
  _pre
  button_home
fi
%>
<%in _footer.cgi %>
