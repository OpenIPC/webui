#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleSshKeys"

function saveKey() {
  if [ -n "$(fw_printenv key_${1})" ]; then
    flash_save "warning" "${1} $tMsgSshKeyExists"
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
    saveKey "ecdsa"
    saveKey "rsa"
    redirect_to "/cgi-bin/ssh-keys.cgi"
    ;;
  restore)
    restoreKey "ecdsa"
    restoreKey "rsa"
    redirect_to "/cgi-bin/ssh-keys.cgi"
    ;;
  delete)
    deleteKey "ecdsa"
    deleteKey "rsa"
    redirect_to "/cgi-bin/ssh-keys.cgi"
    ;;
  *)
%>
<%in _header.cgi %>
<div class="row row-cols-1 row-cols-md-2 row-cols-xl-3 g-4 mb-4">
  <div class="col">
    <div class="card h-100">
      <div class="card-body">
        <form action="/cgi-bin/ssh-keys.cgi" method="post">
          <p><%= $tMsgSshKeyBackup %></p>
          <button type="submit" name="action" value="backup" class="btn btn-danger"><%= $tButtonSshKeyBackup %></button>
        </form>
      </div>
    </div>
  </div>
  <div class="col">
    <div class="card h-100">
      <div class="card-body">
        <p><%= $tMsgSshKeyRestore %></p>
        <form action="/cgi-bin/ssh-keys.cgi" method="post">
          <button type="submit" name="action" value="restore" class="btn btn-danger"><%= $tButtonSshKeyRestore %></button>
        </form>
      </div>
    </div>
  </div>
  <div class="col">
    <div class="card h-100">
      <div class="card-body">
        <p><%= $tMsgSshKeyDelete %></p>
        <form action="/cgi-bin/ssh-keys.cgi" method="post">
          <button type="submit" name="action" value="delete" class="btn btn-danger"><%= $tButtonSshKeyDelete %></button>
        </form>
      </div>
    </div>
  </div>
</div>

<div class="alert alert-secondary" style="overflow-wrap: anywhere;">
<% fw_printenv key_ecdsa %>
</div>

<div class="alert alert-secondary" style="overflow-wrap: anywhere;">
<% fw_printenv key_rsa %>
</div>

<%in _footer.cgi %>
<% esac %>
