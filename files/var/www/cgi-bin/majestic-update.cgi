#!/usr/bin/haserl
<%in p/common.cgi %>
<%
check_url() {
  status_code=$(curl --silent --head $mj_bz2_url)
  status_code=$(echo "$status_code" | grep "HTTP/1.1" | cut -d' ' -f2)
  [ "$status_code" = "200" ] && return=1
}

page_title="Updating Majestic"
mj_bz2_url="http://openipc.s3-eu-west-1.amazonaws.com/majestic.${soc_family}.${fw_variant}.master.tar.bz2"
mj_bz2_file=/tmp/majestic.tar.bz2
mj_tmp_file=/tmp/majestic

if [ ! -f "/rom/${mj_bin_file}" ]; then
  error="Majestic is not supported on this system."
elif [ check_url -ne 1 ]; then
  error="Cannot retrieve update from server."
else
  free_space=$(df | grep $overlay_root | xargs | cut -d' ' -f4)
  mj_filesize_old=0
  [ -f "${$overlay_root}${mj_bin_file}" ] && mj_filesize_old=$(ls -s $mj_bin_file | xargs | cut -d' ' -f1)
  available_space=$(( $free_space + $mj_filesize_old - 1 ))

  log="curl -s -k -L -o ${mj_bz2_file} ${mj_bz2_url}\n"
  log="${log}$(curl -s -k -L -o $mj_bz2_file $mj_bz2_url 2>&1)"
  log="${log}bunzip2 -c ${mj_bz2_file} | tar -x -C /tmp/ ./majestic\n"
  log="${log}$(bunzip2 -c $mj_bz2_file | tar -x -C /tmp/ ./majestic 2>&1)"
  if [ $? -ne 0 ]; then
    error="Cannot extract Majestic archive."
    log="${log}rm -f ${mj_bz2_file}\n"
    log="${log}$(rm -f $mj_bz2_file 2>&1)"
    log="${log}rm -f ${mj_tmp_file}\n"
    log="${log}$(rm -f $mj_tmp_file 2>&1)"
  else
#    mj_filesize_new=$(curl https://openipc.s3-eu-west-1.amazonaws.com/majestic.${soc_family}.master.tar.meta)
    mj_filesize_new=$(ls -s $mj_tmp_file | xargs | cut -d' ' -f1)
    if [ $mj_filesize_new -gt $available_space ]; then
      error="Not enough space to update Majestic. ${mj_filesize_new} KB > ${available_space} KB."
      log="${log}rm -f ${mj_tmp_file}\n"
      log="${log}$(rm -f $mj_tmp_file 2>&1)"
    fi
  fi
  log="${log}rm -f ${mj_bz2_file}\n"
  log="${log}$(rm -f $mj_bz2_file 2>&1)"
fi
%>
<%in p/header.cgi %>
<%
if [ -n "$error" ]; then
  report_error "$error"
  report_log "$log"
else
%>
<pre class="bg-light p-4 log-scroll">
<%
e "$log"
e "killall majestic"
e "$(killall majestic 2>&1)"
e "mv -f ${mj_tmp_file} ${mj_bin_file}"
e "$(mv -f $mj_tmp_file $mj_bin_file 2>&1)"
e "Rebooting..."
e "$(reboot)"
%>
</pre>
<% fi %>
<%in p/footer.cgi %>
