#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleMajesticDebug"

get_software_info

if [ ! -f /rom/${mj_bin_file} ]; then
  flash_save "danger" "$tMsgMajesticIsNotSupported"
  redirect_to "/cgi-bin/status.cgi"
fi

conf_file=/etc/coredump.config

if [ "$REQUEST_METHOD" == "POST" ]; then
  ### Assigning values
  coredump_savedumps="$POST_coredump_enabled"
  coredump_haveconsent="$POST_coredump_consent"
  coredump_send2devs="$POST_coredump_send2devs"
  coredump_contact_name="$POST_coredump_name"
  coredump_contact_email="$POST_coredump_email"
  coredump_contact_telegram="$POST_coredump_telegram"
  coredump_send2tftp="$POST_coredump_send2tftp"
  coredump_tftphost="$POST_coredump_tftphost"
  coredump_send2ftp="$POST_coredump_send2ftp"
  coredump_ftphost="$POST_coredump_ftphost"
  coredump_ftppath="$POST_coredump_ftppath"
  coredump_ftpuser="$POST_coredump_ftpuser"
  coredump_ftppass="$POST_coredump_ftppass"
  coredump_save4web="$POST_coredump_save4web"
  coredump_localpath="$POST_coredump_localpath"

  ### Normalization
  # strip trailing slashes, if any
  coredump_localpath="$(echo "$coredump_localpath" | sed s/^\\/// | sed s/\\/$//)"
  coredump_ftppath="$(echo "$coredump_ftppath" | sed s/^\\/// | sed s/\\/$//)"

  ### Validation
  if [ "$coredump_savedumps" = "true" ]; then
    if [ ! "$coredump_haveconsent" = "true" ]; then
      error="$tMjDebugErrorConsent"
    else
      if [ "$coredump_send2tftp" = "true" ]; then
        [ -z "$coredump_tftphost" ] && error="$tMjDebugErrorTftpHostEmpty"
      fi
      if [ "$coredump_save4web" = "true" ]; then
        [ -z "$coredump_localpath" ] && error="$tMjDebugErrorLocalPathEmpty"
      fi
    fi
  fi

  if [ -z "$error" ]; then
    echo "# /etc/coredump.config
savedumps=${coredump_savedumps}
haveconsent=${coredump_haveconsent}
contact_name=${coredump_contact_name}
contact_email=${coredump_contact_email}
contact_telegram=${coredump_contact_telegram}
send2devs=${coredump_send2devs}
send2tftp=${coredump_send2tftp}
tftphost=${coredump_tftphost}
send2ftp=${coredump_send2ftp}
ftphost=${coredump_ftphost}
ftppath=${coredump_ftppath}
ftpuser=${coredump_ftpuser}
ftppass=${coredump_ftppass}
save4web=${coredump_save4web}
localpath=${coredump_localpath}
" > /etc/coredump.config
    flash_save "success" "$tMjDebugConfigUpdated"
    redirect_to "/cgi-bin/majestic-debug.cgi"
  fi
else
  coredump_enabled=$(grep ^savedumps $conf_file | cut -d= -f2)
  coredump_consent=$(grep ^haveconsent $conf_file | cut -d= -f2)
  coredump_name=$(grep ^contact_name $conf_file | cut -d= -f2)
  coredump_email=$(grep ^contact_email $conf_file | cut -d= -f2)
  coredump_telegram=$(grep ^contact_telegram $conf_file | cut -d= -f2)
  coredump_send2devs=$(grep ^send2devs $conf_file | cut -d= -f2)
  coredump_send2tftp=$(grep ^send2tftp $conf_file | cut -d= -f2)
  coredump_tftphost=$(grep ^tftphost $conf_file | cut -d= -f2)
  coredump_send2ftp=$(grep ^send2ftp $conf_file | cut -d= -f2)
  coredump_ftphost=$(grep ^ftphost $conf_file | cut -d= -f2)
  coredump_ftppath=$(grep ^ftppath $conf_file | cut -d= -f2)
  coredump_ftpuser=$(grep ^ftpuser $conf_file | cut -d= -f2)
  coredump_ftppass=$(grep ^ftppass $conf_file | cut -d= -f2)
  coredump_save4web=$(grep ^save4web $conf_file | cut -d= -f2)
  coredump_localpath=$(grep ^localpath $conf_file | cut -d= -f2)
  if [ -z "$coredump_localpath" ]; then
    if [ -d "/mnt/mmc" ]; then
      coredump_localpath="/mnt/mmc"
    else
      coredump_localpath="/root"
    fi
  fi
fi
%>
<%in _header.cgi %>
<%
if [ -n "$error" ]; then
  report_error "$error"
fi

if [ -z "$(grep sendcoredump.sh /etc/init.d/S95hisilicon)" ]; then
  alert "$tMsgCoreDumpModificationRequired" "warning"
fi

form_ "/cgi-bin/majestic-debug.cgi" "post"
  div_ "class=\"row row-cols-1 row-cols-lg-2 row-cols-xl-3 g-3 mb-4\""
    col_first
      card_ "Last dumping log"
        [ -f /root/coredump.log ] && pre "$(cat /root/coredump.log)"
      _card
      card_ "$tHeaderMjDebug"
        field_switch "coredump_enabled"
        field_text "coredump_name"
        field_text "coredump_email"
        field_text "coredump_telegram"
        field_switch "coredump_consent"
      _card
      card_ "$tHeaderMjDebugUploadS3"
        field_switch "coredump_send2devs"
      _card
    col_next
      card_ "$tHeaderMjDebugUploadTftp"
        field_switch "coredump_send2tftp"
        field_text "coredump_tftphost"
      _card
      card_ "$tHeaderMjDebugUploadFtp"
        field_switch "coredump_send2ftp"
        field_text "coredump_ftphost"
        field_text "coredump_ftppath"
        field_text "coredump_ftpuser"
        field_password "coredump_ftppass"
      _card
      card_ "$tHeaderMjDebugSave4Web"
        field_switch "coredump_save4web"
        field_text "coredump_localpath"
        [ -f "${coredump_localpath}/coredump.tgz" ] && alert "$tMsgCoreDumpExists" "danger"
      _card
    col_next
      alert "$tAlertMjDebugDescription" "info"
    col_last
  _div

  button_submit "$tButtonFormSubmit" "primary mb-4"
_form

%>
<%in _footer.cgi %>
