#!/usr/bin/haserl
<%in _common.cgi %>
<%
check_url() {
  status_code=$(curl --silent --head ${mj_bz2_url})
  status_code=$(echo "$status_code" | grep "HTTP/1.1" | cut -d " " -f 2)
  [ ${status_code} = "200" ] && return=1
}

get_hardware_info
get_firmware_info
get_software_info

page_title="$tPageTitleMajesticGithub"
mj_bz2_url="http://openipc.s3-eu-west-1.amazonaws.com/majestic.${soc_family}.${fw_variant}.master.tar.bz2"
mj_bz2_file="/tmp/majestic.tar.bz2"
mj_tmp_file="/tmp/majestic"

if [ ! -f /rom/${mj_bin_file} ]; then
  error="$tMsgMajesticIsNotSupported"
elif [ check_url -ne 1 ]; then
  error="$tMsgCannotRetrieveUpdate"
else
  free_space=$(df | grep /overlay | xargs | cut -d" " -f4)
  mj_filesize_old=0
  [ -f /overlay/root/${mj_bin_file} ] && mj_filesize_old=$(ls -s ${mj_bin_file} | xargs | cut -d " " -f 1)
  available_space=$(( $free_space + $mj_filesize_old - 1 ))

  log="curl -s -k -L -o ${mj_bz2_file} ${mj_bz2_url}\n"
  log="${log}$(curl -s -k -L -o ${mj_bz2_file} ${mj_bz2_url} 2>&1)"
  log="${log}bunzip2 -c ${mj_bz2_file} | tar -x -C /tmp/ ./majestic\n"
  log="${log}$(bunzip2 -c ${mj_bz2_file} | tar -x -C /tmp/ ./majestic 2>&1)"
  if [ $? -ne 0 ]; then
    error="$tMsgCannotExtractMajestic"
    log="${log}rm -f ${mj_bz2_file}\n"
    log="${log}$(rm -f ${mj_bz2_file} 2>&1)"
    log="${log}rm -f ${mj_tmp_file}\n"
    log="${log}$(rm -f ${mj_tmp_file} 2>&1)"
  else
#    mj_filesize_new=$(curl https://openipc.s3-eu-west-1.amazonaws.com/majestic.${soc_family}.master.tar.meta)
    mj_filesize_new=$(ls -s ${mj_tmp_file} | xargs | cut -d " " -f 1)
    if [ $mj_filesize_new -gt $available_space ]; then
      error="$tMsgNoSpaceToExtractMajestic ${mj_filesize_new} KB > ${available_space} KB."
      log="${log}rm -f ${mj_tmp_file}\n"
      log="${log}$(rm -f ${mj_tmp_file} 2>&1)"
    fi
  fi
  log="${log}rm -f ${mj_bz2_file}\n"
  log="${log}$(rm -f ${mj_bz2_file} 2>&1)"
fi
%>
<%in _header.cgi %>
<%
if [ ! -z "$error" ]; then
  report_error "$error"
  report_log "$log"
else
%>
<pre class="bg-light p-4 log-scroll">
<%
  echo -e "$log"
  echo "killall majestic"
  echo "$(killall majestic 2>&1)"
  echo "mv -f ${mj_tmp_file} ${mj_bin_file}"
  echo "$(mv -f ${mj_tmp_file} ${mj_bin_file} 2>&1)"
  echo "$tMsgRebooting"
  echo "$(reboot)"
fi
%>
</pre>
<%in _footer.cgi %>
