#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPT_SshKeys"

function readKey() {
  [ -n "$(fw_printenv key_${1})" ] && alert "$(fw_printenv key_${1})" "secondary" "style=\"overflow-wrap: anywhere;\""
}

function saveKey() {
  if [ -n "$(fw_printenv key_${1})" ]; then
    flash_save "danger" "${1} $tMsgSshKeyExists"
  else
    fw_setenv key_${1} $(dropbearconvert dropbear openssh /etc/dropbear/dropbear_${1}_host_key - 2>/dev/null | base64 | tr -d '\n')
  fi
}

function restoreKey() {
  if [ -z "$(fw_printenv key_${1})" ]; then
    flash_save "danger" "${1} $tMsgSshKeyNotFound"
  else
    fw_printenv key_${1} | sed s/^key_${1}=// | base64 -d | dropbearconvert openssh dropbear - /etc/dropbear/dropbear_${1}_host_key
    flash_save "success" "${1} $tMsgSshKeyRestored"
  fi
}

function deleteKey() {
  if [ -z "$(fw_printenv key_${1})" ]; then
    flash_save "danger" "${1} $tMsgSshKeyNotFound"
  else
    fw_setenv key_${1}
    flash_save "success" "${1} $tMsgSshKeyDeleted"
  fi
}

case "$POST_action" in
  backup)
    saveKey "ed25519"
    redirect_to "/cgi-bin/ssh-keys.cgi"
    ;;
  restore)
    restoreKey "ed25519"
    redirect_to "/cgi-bin/ssh-keys.cgi"
    ;;
  delete)
    deleteKey "ed25519"
    redirect_to "/cgi-bin/ssh-keys.cgi"
    ;;
  *)
%>
<%in _header.cgi %>
<%
render "ssh-keys"
readKey "ed25519"
%>
<%in p/footer.cgi %>
<% esac %>
