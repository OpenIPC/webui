<%
row_ "row-cols-1 row-cols-lg-2 g-3 mb-3"
  col_card_ "$tHD_MjBackup"
    p "$tMjBackupInfo"
    button_link_to "$tB_MjBackup" "/cgi-bin/majestic-config-backup.cgi" "primary"
  _col_card
  col_card_ "$tHD_MjRestore"
    p "$tMjRestoreInfo"
    form_upload_ "/cgi-bin/majestic-config-restore.cgi"
      field_file "mj_restore_file"
      button_submit "$tB_MjRestore" "danger"
    _form
  _col_card
  col_card_ "$tHD_MjChanges"
    p "$tMjChangesInfo"
    button_link_to "$tB_MjChanges" "/cgi-bin/majestic-config-compare.cgi" "primary"
  _col_card
  col_card_ "$tHD_MjReset"
    p "$tMjResetInfo"
    button_link_to "$tB_MjReset" "/cgi-bin/majestic-config-reset.cgi" "danger"
  _col_card
_row
%>
