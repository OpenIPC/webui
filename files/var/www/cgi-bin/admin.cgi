#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="admin"
page_title="Admin profile"
params="name email telegram"

tmp_file=/tmp/${plugin}.conf
config_file="${ui_config_dir}/${plugin}.conf"
[ ! -f "$config_file" ] && touch $config_file

if [ "POST" = "$REQUEST_METHOD" ]; then
  # parse values from parameters
  for _p in $params; do
    eval ${plugin}_${_p}=\$POST_${plugin}_${_p}
    sanitize "${plugin}_${_p}"
  done; unset _p

  [ -z "$admin_name"  ] && flash_append "danger" "Admin name cannot be empty." && error=1
  [ -z "$admin_email" ] && flash_append "danger" "Admin email cannot be empty." && error=1
  # [ -z "$admin_telegram" ] && error="Admin telegram username cannot be empty."

  # add @ to Telegram username, if missed
  [ -n "$admin_telegram" ] && [ "${admin_telegram:0:1}" != "@" ] && admin_telegram="@$admin_telegram"

  if [ -z "$error" ]; then
    # create temp config file
    :> $tmp_file
    for _p in $params; do
      echo "${plugin}_${_p}=\"$(eval echo \$${plugin}_${_p})\"" >> $tmp_file
    done; unset _p
    mv $tmp_file $config_file

    update_caminfo
    redirect_back "success" "Admin profile updated."
  fi
else
  include $config_file
fi
%>
<%in p/header.cgi %>

<div class="row">
  <div class="col col-md-6 col-lg-4 col-xxl-3">
    <h3>Settings</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "update" %>
      <% field_text "admin_name" "Admin's full name" "will be used for sending emails" %>
      <% field_text "admin_email" "Admin's email address" %>
      <% field_text "admin_telegram" "Admin's nick on Telegram" %>
      <% button_submit %>
    </form>
  </div>
  <div class="col col-md-6 col-lg-8 col-xxl-9">
    <% ex "cat $config_file" %>
  </div>
</div>

<%in p/footer.cgi %>
