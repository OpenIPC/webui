<%
row_ "row-cols-1 row-cols-md-2 row-cols-xl-3 g-3 mb-3"
  col_card_ "Key Backup"
    form_ "/cgi-bin/ssh-keys.cgi"
      p "$tMsgSshKeyBackup"
      button_submit_action "backup" "$tB_SshKeyBackup"
    _form
  _col_card
  col_card_ "Key Restore"
    p "$tMsgSshKeyRestore"
    form_ "/cgi-bin/ssh-keys.cgi"
      button_submit_action "restore" "$tB_SshKeyRestore"
    _form
  _col_card
  col_card_ "Key Delete"
    p "$tMsgSshKeyDelete"
    form_ "/cgi-bin/ssh-keys.cgi"
      button_submit_action "delete" "$tB_SshKeyDelete"
    _form
  _col_card
_row
%>
