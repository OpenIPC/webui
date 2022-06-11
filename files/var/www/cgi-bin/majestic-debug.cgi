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
  savedumps="$POST_coredump_enabled"
  haveconsent="$POST_coredump_consent"
  send2devs="$POST_coredump_send2devs"
  contact_name="$POST_coredump_name"
  contact_email="$POST_coredump_email"
  contact_telegram="$POST_coredump_telegram"
  send2tftp="$POST_coredump_send2tftp"
  tftphost="$POST_coredump_tftphost"
  send2ftp="$POST_coredump_send2ftp"
  ftphost="$POST_coredump_ftphost"
  ftppath="$POST_coredump_ftppath"
  ftpuser="$POST_coredump_ftpuser"
  ftppass="$POST_coredump_ftppass"
  save4web="$POST_coredump_save4web"

  ### Normalization
  ftppath="$(echo "$ftppath" | sed s/^\\/// | sed s/\\/$//)" # strip trailing slashes, if any

  ### Validation
  if [ "$savedumps" == "true" ]; then
    if [ ! "$haveconsent" == "true" ]; then
      error="$tMjDebugErrorConsent"
    else
      if [ "$send2tftp" == "true" ]; then
        [ -z "$tftphost" ] && error="$tMjDebugErrorTftpHostEmpty"
      fi
    fi
  fi

  if [ -n "$error" ]; then
    flash_save "danger" "$error"
  else
    echo "# /etc/coredump.config
savedumps=${savedumps}
haveconsent=${haveconsent}
contact_name=${contact_name}
contact_email=${contact_email}
contact_telegram=${contact_telegram}
send2devs=${send2devs}
send2tftp=${send2tftp}
tftphost=${tftphost}
send2ftp=${send2ftp}
ftphost=${ftphost}
ftppath=${ftppath}
ftpuser=${ftpuser}
ftppass=${ftppass}
save4web=${save4web}
" > /etc/coredump.config
    flash_save "success" "$tMjDebugConfigUpdated"
    redirect_to "/cgi-bin/majestic-debug.cgi"
  fi
fi

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
%>
<%in _header.cgi %>
<%
if [ -n "$error" ]; then
  report_error "$error"
  report_log "$log"
else
  [ -z "$(grep sendcoredump.sh /etc/init.d/S95hisilicon)" ] && alert "$tMsgCoreDumpModificationRequired" "warning"

  form_ "/cgi-bin/majestic-debug.cgi" "post"
    div_ "class=\"row row-cols-1 row-cols-xl-2 g-4 mb-4\""
      col_first
        alert "$tAlertMjDebugDescription" "info"
        card_ "$tHeaderMjDebug"
          field_switch "coredump_enabled"
          field_text "coredump_name"
          field_text "coredump_email"
          field_text "coredump_telegram"
          field_checkbox "coredump_consent"
        _card
      col_next
        card_ "$tHeaderMjDebugUploadS3"
          field_switch "coredump_send2devs"
        _card
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
        _card
        [ -f "/root/coredump.tgz" ] && alert "$tMsgCoreDumpExists" "danger"
      col_last
    _div
    button_submit "$tButtonFormSubmit" "primary"
  _form
fi
%>
<%in _footer.cgi %>
