#!/usr/bin/haserl --upload-limit=100 --upload-dir=/tmp
<%in p/common.cgi %>
<%
if [ "POST" = "$REQUEST_METHOD" ]; then
  case "$POST_action" in
  access)
    new_password="$POST_webui_password"
    [ -z "$new_password" ] && error="Password cannot be empty!"
    [ "$password_fw" = "$new_password" ] && error="You cannot use default password!"
    [ -n "$(echo "$new_password" | grep " ")" ] && error="Password cannot have spaces!"
    [ "5" -ge "${#new_password}" ] && error="Password cannot be shorter than 6 characters!"

#    new_password_confirmation="$POST_webui_password_confirmation"
#    [ -z "$new_password_confirmation" ] && error="Password requires confirmation!"
#    [ "$new_password" != "$new_password_confirmation" ] && error="Password does not match its confirmation!"

    if [ -z "$error" ]; then
      sed -i s/:admin:.*/:admin:${new_password}/ /etc/httpd.conf
      redirect_to $SCRIPT_NAME "success" "Password updated."
    else
      redirect_to $SCRIPT_NAME "danger" "$error"
    fi
    ;;

  locale)
    locale="$POST_webui_language" # set language.
    # upload new language and switch to it. overrides aboveset language.
    _fname="$POST_webui_locale_file_name"
    if [ -n "$_fname" ]; then
      mv "$POST_webui_locale_file_path" /var/www/lang/$_fname
      locale=${_fname%%.*}
    fi
    # save new language settings and reload locale
    [ -z "$locale" ] && locale="en"
    echo "$locale" > /etc/web_locale
    reload_locale
    redirect_to $SCRIPT_NAME "success" "Locale updated."
    ;;

  *)
    redirect_to $SCRIPT_NAME "danger" "UNKNOWN ACTION: $POST_action"
    ;;
  esac
fi

page_title="Web Interface Settings"

# data for form fields
webui_username="admin"
webui_language="$locale"

tOptions_webui_language="en|English"
for i in /var/www/lang/; do
  code="$(basename $i)"; code="${code%%.sh}"
  name="$(sed -n 2p $i|sed "s/ /_/g"|cut -d: -f2)"
  tOptions_webui_language="${tOptions_webui_language},${code}|${name}"
done
%>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-md-2 row-cols-xl-3 g-4">
  <div class="col">
    <h3>Access</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "access" %>
      <p class="string">
        <label for="webui_username" class="form-label">Username</label>
        <input type="text" id="webui_username" name="webui_username" value="admin" class="form-control" autocomplete="username" disabled>
      </p>
      <% field_password "webui_password" "Password" %>
      <% # field_password "webui_password_confirmation" "Confirm Password" %>
      <% button_submit %>
    </form>
  </div>
  <div class="col">
    <h3>Locale</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post" enctype="multipart/form-data">
      <% field_hidden "action" "locale" %>
      <% field_select "webui_language" "Interface Language" "en|English" %>
      <% field_file "webui_locale_file" "Locale file" %>
      <% button_submit %>
    </form>
  </div>

<% if [ "$debug" -ge "1" ]; then %>
  <div class="col">
    <h3>Configuration</h3>
    <%
    ex "cat /etc/httpd.conf"
    #ex "echo \$locale"
    #ex "cat /etc/web_locale"
    #ex "ls /var/www/lang/"
    %>
  </div>
<% fi %>
</div>

<%in p/footer.cgi %>
