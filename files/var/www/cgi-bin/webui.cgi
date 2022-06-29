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

  init)
    update_caminfo
    redirect_back
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

page_title="Web Interface"

# data for form fields
webui_username="admin"
webui_language="$locale"

webui_version="master"
[ -n "$ui_version" ] && webui_version="$(echo "$ui_version" | cut -d+ -f1)"

tOptions_webui_language="en|English"
for i in /var/www/lang/; do
  code="$(basename $i)"; code="${code%%.sh}"
  name="$(sed -n 2p $i|sed "s/ /_/g"|cut -d: -f2)"
  tOptions_webui_language="${tOptions_webui_language},${code}|${name}"
done
%>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-md-2 row-cols-xl-4 g-4">
  <div class="col">
    <h3>Package</h3>
    <dl class="small list">
      <dt>Installed</dt><dd><%= $ui_version %></dd>
      <dt>Stable</dt><dd id="microbe-web-master-ver"></dd>
      <dt>Unstable</dt><dd id="microbe-web-dev-ver"></dd>
    </dl>
    <h4>Install update</h4>
    <form action="webui-update.cgi" method="post">
      <input type="hidden" name="action" value="update">
      <p class="select input-group">
        <label for="web_version" class="input-group-text">Branch</label>
        <select class="form-select" id="web_version" name="web_version" required>
          <option value="">Choose...</option>
          <option value="master"<%= [ "master" = "$webui_version" ] && echo " selected" %>>Stable</option>
          <option value="dev"<%= [ "dev" = "$webui_version" ] && echo " selected" %>>Development</option>
        </select>
      </p>
      <p class="boolean form-check">
        <input type="checkbox" name="web_verbose" id="web_verbose" value="true" class="form-check-input">
        <label for="web_verbose" class="form-label">Verbose output.</label>
      </p>
      <p class="boolean form-check">
        <input type="checkbox" name="web_enforce" id="web_enforce" value="true" class="form-check-input">
        <label for="web_enforce" class="form-label">Install even if the same version.</label>
      </p>
      <p class="boolean form-check">
        <input type="hidden" name="fw_noreboot" id="web_noreboot-false" value="false">
        <input type="checkbox" name="fw_noreboot" id="web_noreboot" value="true" class="form-check-input">
        <label for="web_noreboot" class="form-label">Do not reboot after upgrade.</label>
      </p>
      <p class="mt-2"><input type="submit" class="btn btn-warning" value="<%= $t_btn_update %>"></p>
    </form>
  </div>

  <div class="col">
    <h3>Access</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <input type="hidden" name="action" value="access">
      <p class="string">
        <label for="webui_username" class="form-label">Username</label>
        <input type="text" id="webui_username" name="webui_username" value="admin" class="form-control" autocomplete="username" disabled>
      </p>
      <p class="password">
        <label for="webui_password" class="form-label">Password</label>
        <span class="input-group">
          <input type="password" id="webui_password" name="webui_password" class="form-control" placeholder="K3wLHaZk3R!" required>
          <label class="input-group-text"><input class="form-check-input me-1" type="checkbox" data-for="webui_password"> show</label>
        </span>
      </p>
      <!--
      <p class="password">
        <label for="webui_password_confirmation" class="form-label">Confirm Password</label>
        <span class="input-group">
          <input type="password" id="webui_password_confirmation" name="webui_password_confirmation" class="form-control" placeholder="K3wLHaZk3R!">
        <label class="input-group-text"><input class="form-check-input me-1" type="checkbox" data-for="webui_password_confirmation"> show</label>
        </span>
      </p>
      -->
      <p class="mt-2"><input type="submit" class="btn btn-primary" value="Save changes"></p>
    </form>
  </div>

  <div class="col">
    <h3>Locale</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post" enctype="multipart/form-data">
      <input type="hidden" name="action" value="locale">
      <p class="select">
        <label for="webui_language" class="form-label">Language</label>
        <select class="form-select" id="webui_language" name="webui_language">
          <option value="en" selected="">English</option>
          <% # FIXME: add more locales %>
        </select>
      </p>
      <p class="file">
        <label for="webui_locale_file" class="form-label">Locale file</label>
        <input type="file" id="webui_locale_file" name="webui_locale_file" class="form-control">
      </p>
      <p class="mt-2"><input type="submit" class="btn btn-primary" value="Save changes"></p>
    </form>
  </div>

  <div class="col">
    <h3>Configuration</h3>
    <%
    ex "cat /etc/httpd.conf"
    #ex "echo \$locale"
    #ex "cat /etc/web_locale"
    #ex "ls /var/www/lang/"
    %>
  </div>
</div>

<script>
const GH_URL="https://github.com/OpenIPC/";
const GH_API="https://api.github.com/repos/OpenIPC/";

function checkUpdates() {
  queryBranch('microbe-web', 'master');
  queryBranch('microbe-web', 'dev');
}

function queryBranch(repo, branch) {
  var oReq = new XMLHttpRequest();
  oReq.addEventListener("load", function(){
    const d = JSON.parse(this.response);
    const sha_short = d.commit.sha.slice(0,7);
    const date = d.commit.commit.author.date.slice(0,10);
    const link = document.createElement('a');
    link.href = GH_URL + repo + '/commits/' + branch;
    link.target = '_blank';
    link.textContent = branch + '+' + sha_short + ', ' + date;
    const el = $('#' + repo + '-' + branch + '-ver').appendChild(link);
  });
  oReq.open("GET", GH_API + repo + '/branches/' + branch);
  oReq.setRequestHeader("Authorization", "Basic " + btoa("<%= "${GITHUB_USERNAME}:${GITHUB_TOKEN}" %>"));
  oReq.send();
}

window.addEventListener('load', checkUpdates);
</script>
<%in p/footer.cgi %>
