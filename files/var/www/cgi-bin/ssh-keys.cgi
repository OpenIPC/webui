#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$t_sshkey_0"

function readKey() {
  [ -n "$(fw_printenv key_${1})" ] && alert "$(fw_printenv key_${1})" "secondary" "style=\"overflow-wrap: anywhere;\""
}

function saveKey() {
  if [ -n "$(fw_printenv key_${1})" ]; then
    flash_save "danger" "${1} $t_sshkey_a"
  else
    fw_setenv key_${1} $(dropbearconvert dropbear openssh /etc/dropbear/dropbear_${1}_host_key - 2>/dev/null | base64 | tr -d '\n')
  fi
}

function restoreKey() {
  if [ -z "$(fw_printenv key_${1})" ]; then
    flash_save "danger" "${1} $t_sshkey_b"
  else
    fw_printenv key_${1} | sed s/^key_${1}=// | base64 -d | dropbearconvert openssh dropbear - /etc/dropbear/dropbear_${1}_host_key
    flash_save "success" "${1} $t_sshkey_c"
  fi
}

function deleteKey() {
  if [ -z "$(fw_printenv key_${1})" ]; then
    flash_save "danger" "${1} $t_sshkey_d"
  else
    fw_setenv key_${1}
    flash_save "success" "${1} $t_sshkey_e"
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
<div class="row row-cols-1 row-cols-md-2 row-cols-xl-3 g-3 mb-3">
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_sshkey_1 %></div>
<div class="card-body">
<form action="/cgi-bin/ssh-keys.cgi" method="post" autocomplete="off">
<p><%= $t_sshkey_2 %></p>
<button class="btn btn-danger" name="action" type="submit" value="backup"><%= $t_sshkey_3 %></button>
</form>
</div>
</div>
</div>
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_sshkey_4 %></div>
<div class="card-body">
<p><%= $t_sshkey_5 %></p>
<form action="/cgi-bin/ssh-keys.cgi" method="post" autocomplete="off" autocomplete="off">
<button class="btn btn-danger" name="action" type="submit" value="restore"><%= $t_sshkey_6 %></button>
</form>
</div>
</div>
</div>
<div class="col">
<div class="card mb-3 h-100">
<div class="card-header"><%= $t_sshkey_7 %></div>
<div class="card-body">
<p><%= $t_sshkey_8 %></p>
<form action="/cgi-bin/ssh-keys.cgi" method="post">
<button class="btn btn-danger" name="action" type="submit" value="delete"><%= $t_sshkey_9 %></button>
</form>
</div>
</div>
</div>
</div>
<% readKey "ed25519" %>
<%in p/footer.cgi %>
<% esac %>
