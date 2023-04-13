#!/usr/bin/haserl --upload-limit=100 --upload-dir=/tmp
<%in p/common.cgi %>
<%
plugin="webui"
plugin_name="User interface settings"
page_title="Web Interface Settings"

tmp_file=/tmp/${plugin}.conf

config_file="${ui_config_dir}/${plugin}.conf"
[ ! -f "$config_file" ] && touch $config_file

locale_file=/etc/webui/locale

if [ "POST" = "$REQUEST_METHOD" ]; then
  case "$POST_action" in
  access)
    new_password="$POST_ui_password_new"
    [ -z "$new_password" ] && error="Password cannot be empty!"
    [ "$ui_password_fw" = "$new_password" ] && error="You cannot use default password!"
    [ -n "$(echo "$new_password" | grep " ")" ] && error="Password cannot have spaces!"
    [ "5" -ge "${#new_password}" ] && error="Password cannot be shorter than 6 characters!"

    [ -n "$error" ] && redirect_to $SCRIPT_NAME "danger" "$error"

    sed -i "s/:admin:.*/:admin:$(mkpasswd $new_password)/" /etc/httpd.conf
    echo "root:${new_password}" | chpasswd
    update_caminfo

    redirect_to "/" "success" "Password updated."
    ;;

  interface)
    params="level theme"
    for _p in $params; do
      eval ${plugin}_${_p}=\$POST_${plugin}_${_p}
      sanitize "${plugin}_${_p}"
    done; unset _p

    [ -z "$webui_level" ] && webui_level="user"

    if [ -z "$error" ]; then
      # create temp config file
      :>$tmp_file
      for _p in $params; do
        echo "${plugin}_${_p}=\"$(eval echo \$${plugin}_${_p})\"" >>$tmp_file
      done; unset _p
      mv $tmp_file $config_file

      update_caminfo
      redirect_back "success" "${plugin_name} config updated."
    fi
    ;;

  locale)
    locale="$POST_ui_language" # set language.
    # upload new language and switch to it. overrides aboveset language.
    _fname="$POST_ui_locale_file_name"
    if [ -n "$_fname" ]; then
      mv "$POST_ui_locale_file_path" /var/www/lang/$_fname
      locale=${_fname%%.*}
    fi
    # save new language settings and reload locale
    [ -z "$locale" ] && locale="en"
    echo "$locale" >$locale_file
    reload_locale
    update_caminfo
    redirect_to $SCRIPT_NAME "success" "Locale updated."
    ;;

  *)
    redirect_to $SCRIPT_NAME "danger" "UNKNOWN ACTION: $POST_action"
    ;;
  esac
fi

page_title="Web Interface Settings"

# data for form fields
ui_username="admin"
ui_language="$locale"

ui_locales="en|English"
if [ -d /var/www/lang/ ]; then
 for i in $(ls -1 /var/www/lang/); do
    code="$(basename $i)"; code="${code%%.sh}"
    name="$(sed -n 2p $i|sed "s/ /_/g"|cut -d: -f2)"
    ui_locales="${ui_locales},${code}|${name}"
  done
fi
%>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <h3>Access</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "access" %>
      <p class="string">
        <label for="ui_username" class="form-label">Username</label>
        <input type="text" id="ui_username" name="ui_username" value="admin" class="form-control" autocomplete="username" disabled>
      </p>
      <% field_password "ui_password_new" "Password" %>
      <% button_submit %>
    </form>
  </div>
  <div class="col">
    <h3>Interface Details</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "interface" %>
      <% field_select "webui_level" "Level" "user,expert" %>
      <% field_select "webui_theme" "Theme" "light,dark" %>
      <% button_submit %>
    </form>
  </div>
<!--
  <div class="col">
    <h3>Locale</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post" enctype="multipart/form-data">
      <% field_hidden "action" "locale" %>
      <% field_select "ui_language" "Interface Language" "$ui_locales" %>
      <%# field_file "ui_locale_file" "Locale file" %>
      <% button_submit %>
    </form>
  </div>
-->
  <div class="col">
    <h3>Configuration</h3>
    <%
    ex "cat /etc/httpd.conf"
    #ex "echo \$locale"
    #ex "cat $locale_file"
    #ex "ls /var/www/lang/"
    ex "cat $config_file"
    %>
  </div>
</div>

<%in p/footer.cgi %>
