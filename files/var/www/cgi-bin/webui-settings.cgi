#!/usr/bin/haserl --upload-limit=100 --upload-dir=/tmp
<%in p/common.cgi %>
<%
if [ "POST" = "$REQUEST_METHOD" ]; then
  # language routine
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

  # password routine
  new_password="$POST_webui_password"
  new_password_confirmation="$POST_webui_password_confirmation"

  if [ -z "$new_password" ]; then
    error="$t_wui_4"
  elif [ "$password_fw" = "$new_password" ]; then
    error="$t_wui_5"
  elif [ -n "$(echo "$new_password" | grep " ")" ]; then
    error="$t_wui_6"
  elif [ "5" -ge "${#new_password}" ]; then
    error="$t_wui_7"
  elif [ -z "$new_password_confirmation" ]; then
    error="$t_wui_8"
  elif [ "$new_password" != "$new_password_confirmation" ]; then
    error="$t_wui_9"
  fi

  if [ -z "$error" ]; then
    sed -i s/:admin:.*/:admin:${new_password}/ /etc/httpd.conf
    redirect_to $SCRIPT_NAME "success" "Changes saved."
  fi
fi

page_title="$t_wui_0"
tOptions_webui_language="en|English"
for i in /var/www/lang/; do
  code="$(basename $i)"; code="${code%%.sh}"
  name="$(sed -n 2p $i|sed "s/ /_/g"|cut -d: -f2)"
  tOptions_webui_language="${tOptions_webui_language},${code}|${name}"
done

# data for form fields
webui_username="admin"
webui_language="$locale"
%>
<%in p/header.cgi %>
<%
[ -n "$error" ] && report_error "$error"
%>
<form action="/cgi-bin/webui-settings.cgi" method="post" enctype="multipart/form-data">
<div class="row">

<div class="col col-md-6 col-xl-4">
  <h3><%= $t_wui_1 %></h3>
  <p class="string">
    <label for="webui_username" class="form-label">Username</label>
    <input type="text" id="webui_username" name="webui_username" value="admin" class="form-control" autocomplete="username" disabled="">
  </p>
  <p class="password">
    <label for="webui_password" class="form-label">Password</label>
    <span class="input-group">
      <input type="password" id="webui_password" name="webui_password" class="form-control" placeholder="K3wLHaZk3R!">
      <label class="input-group-text"><input class="form-check-input me-1" type="checkbox" data-for="webui_password">  show</label>
    </span>
  </p>
  <p class="password">
    <label for="webui_password_confirmation" class="form-label">Confirm Password</label>
    <span class="input-group">
      <input type="password" id="webui_password_confirmation" name="webui_password_confirmation" class="form-control" placeholder="K3wLHaZk3R!">
    <label class="input-group-text"><input class="form-check-input me-1" type="checkbox" data-for="webui_password_confirmation">  show</label>
    </span>
  </p>
</div>

<div class="col col-md-6 col-xl-4">
  <h3><%= $t_wui_2 %></h3>
  <p class="select">
    <label for="webui_language" class="form-label">Language</label>
    <select class="form-select" id="webui_language" name="webui_language">
      <option value="en" selected="">English</option>
      <% # %>
    </select>
  </p>
  <p class="file">
    <label for="webui_locale_file" class="form-label">Locale file</label>
    <input type="file" id="webui_locale_file" name="webui_locale_file" class="form-control">
  </p>
</div>

<div class="col col-md-6 col-xl-4">
<h3><%= $t_wui_3 %></h3>
<%
ex "cat /etc/httpd.conf"
ex "echo \$locale"
ex "cat /etc/web_locale"
ex "ls /var/www/lang/"
%>
</div>

</div>
<button type="submit" class="btn btn-primary mt-3"><%= $t_btn_submit %></button>
</form>

<script>
$$('.toggle-password').forEach(el => {
  el.addEventListener('click', (ev) => {
    const type = (ev.target.checked) ? 'type' : 'password';
    $$('input.password').forEach(el => el.type = type);
    $$('.toggle-password').forEach(el => el.checked = ev.target.checked);
    $('#password').focus();
  })
});
</script>
<%in p/footer.cgi %>
