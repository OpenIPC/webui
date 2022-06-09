#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleMajesticMaintenance"
%>
<%in _header.cgi %>
<%
div_ "class=\"row row-cols-1 row-cols-lg-2 g-4 mb-3\""

col_card_ "$tHeaderMjBackup"
  p "$tMjBackupInfo"
  button_link_to "$tButtonMjBackup" "/cgi-bin/majestic-config-backup.cgi"
_col_card

col_card_ "$tHeaderMjRestore"
  p "$tMjRestoreInfo"
  form_ "/cgi-bin/majestic-config-restore.cgi" "post" "enctype=\"multipart/form-data\""
    field_file "mj_restore_file"
    button_submit "$tButtonMjRestore" "danger"
  _form
_col_card

col_card_ "$tHeaderMjChanges"
  p "$tMjChangesInfo"
  button_link_to "$tButtonMjChanges" "/cgi-bin/majestic-config-compare.cgi"
_col_card

col_card_ "$tHeaderMjReset"
  p "$tMjResetInfo"
  button_link_to "$tButtonMjReset" "/cgi-bin/majestic-config-reset.cgi", "danger"
_col_card
_div
%>
<%in _footer.cgi %>
