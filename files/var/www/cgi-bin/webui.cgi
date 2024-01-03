#!/usr/bin/haserl
<%in p/common.cgi %>
<%
if [ "POST" = "$REQUEST_METHOD" ]; then
	case "$POST_action" in
		init)
			update_caminfo
			redirect_back
			;;
		*)
			redirect_to $SCRIPT_NAME "danger" "UNKNOWN ACTION: $POST_action"
			;;
	esac
fi

page_title="Web Interface"

web_branch="master"
[ -n "$ui_version" ] && web_branch="$(echo "$ui_version" | cut -d+ -f1)"
%>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <h3>Version</h3>
    <dl class="list small">
      <dt>Installed</dt><dd><%= $ui_version %></dd>
      <dt>Stable</dt><dd id="webui-master-ver"></dd>
      <dt>Unstable</dt><dd id="webui-dev-ver"></dd>
    </dl>
  </div>
  <div class="col">
    <h3>Upgrade</h3>
  <% if [ -n "$network_gateway" ]; then %>
    <form action="webui-update.cgi" method="post">
      <% field_hidden "action" "update" %>
      <% field_select "web_branch" "Branch" "master:Stable,dev:Development" %>
<% if [ "$debug" -gt 0 ]; then %>
      <% field_text "web_commit" "Commit" "" %>
<% fi %>
      <% field_checkbox "web_verbose" "Verbose output." %>
      <% field_checkbox "web_enforce" "Install even if the same version." %>
      <% field_checkbox "web_noreboot" "Do not reboot after upgrade." %>
      <% button_submit "Install update from GitHub" "warning" %>
    </form>
  <% else %>
    <p class="alert alert-danger">Upgrading requires access to GitHub.</p>
  <% fi %>
  </div>
</div>

<script>
const GH_URL="https://github.com/OpenIPC/";
const GH_API="https://api.github.com/repos/OpenIPC/";

function checkUpdates() {
  queryBranch('webui', 'master');
  queryBranch('webui', 'dev');
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
