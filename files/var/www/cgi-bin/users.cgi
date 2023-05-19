#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="users"
plugin_name="Users"
page_title="Users"

conf_file=/tmp/passwd

if [ -n "$POST_action" ] && [ "$POST_action" = "create" ]; then
  user_name="$POST_user_name"
  user_name_new="$POST_user_name_new"
  user_password="$POST_user_password"
  user_full_name="$POST_user_full_name"
  user_home="$POST_user_home"
  user_shell="$POST_user_shell"
  user_group="$POST_user_group"

  [ -n "$user_name_new" ] && user_name=$user_name_new

  [ -z "$user_name" ] && flash_append "danger" "User name cannot be empty." && error=1
  [ -z "$user_password" ] && flash_append "danger" "User password cannot be empty." && error=1

  if [ -z "$error" ]; then
    if grep -q "^${user_name}:" /etc/passwd; then
      flash_append "warning" "User ${user_name} found."
    else
      adduser ${user_name} -h ${user_home:-/dev/null} -s ${user_shell:-/bin/false} -G ${user_group:-users} -D -g "${user_full_name}"
      if [ $? -eq 0 ]; then
        flash_append "success" "User ${user_name} created."
      else
        flash_append "danger" "Failed to create user ${user_name}." && error=1
      fi
    fi

    if [ -z "$error" ]; then
      result=$(echo "${user_name}:${user_password}" | chpasswd 2>&1)
      if [ $? -eq 0 ]; then
        flash_append "success" "Password for ${user_name} set."
        redirect_back
      else
        flash_append "danger" "$result"
      fi
    fi
  fi
fi

users=$(awk 'BEGIN { FS = ":" } ; { if ($3 > 1000) print $1 }' /etc/passwd)

[ -z "$user_home" ] && user_home="/dev/null"
[ -z "$user_shell" ] && user_shell="/bin/false"
[ -z "$user_group" ] && user_group="users"
%>

<%in p/header.cgi %>

<div class="row g-4 mb-4">
  <div class="col col-lg-4">
    <h3>Settings</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "create" %>
      <% field_select "user_name" "Username" "$users" "<a href=\"#\" id=\"show_new_user\">Create a new user</a>" %>
      <% field_text "user_name_new" "Username" "<a href=\"#\" id=\"hide_new_user\">Select an existing user</a>" %>
      <% field_password "user_password" "Password" %>
      <% field_text "user_full_name" "Full name" %>
      <% field_text "user_home" "Home directory" %>
      <% field_text "user_shell" "Shell" %>
      <% field_text "user_group" "Group" %>
      <% button_submit %>
    </form>
  </div>
  <div class="col col-lg-8">
    <h3>Configuration files</h3>
    <% ex "cat /etc/passwd" %>
    <% ex "cat /etc/shadow" %>
    <% ex "cat /etc/group" %>
  </div>
</div>

<script>
function showNewUser() {
  document.querySelector('#user_full_name').disabled = false;
  document.querySelector('#user_name_new_wrap').classList.remove('d-none');
  document.querySelector('#user_name_wrap').classList.add('d-none');
  document.querySelector('#user_name').value = '';
}

function hideNewUser() {
  document.querySelector('#user_full_name').disabled = true;
  document.querySelector('#user_name_wrap').classList.remove('d-none');
  document.querySelector('#user_name_new_wrap').classList.add('d-none');
  document.querySelector('#user_name_new').value = '';
}

document.querySelector('#show_new_user').addEventListener('click', event => {
  event.preventDefault();
  showNewUser();
});

document.querySelector('#hide_new_user').addEventListener('click', event => {
  event.preventDefault();
  hideNewUser();
});

if (document.querySelector('#user_name_new').value == "") {
  hideNewUser();
} else {
  showNewUser();
}

document.querySelector('#user_home').disabled = true;
document.querySelector('#user_shell').disabled = true;
document.querySelector('#user_group').disabled = true;
</script>

<%in p/footer.cgi %>
