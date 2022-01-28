#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleWebuiSettings"
%>
<%in _header.cgi %>
<div class="row">
<div class="col-md-6 m-auto">
<div class="card">
<div class="card-header"><%= $tHeaderWebuiSettings %></div>
<div class="card-body">
<form action="/cgi-bin/webui-settings-update.cgi" method="post">
<div class="row mb-1">
<label class="col-md-5 form-label" for="username"><%= $tWebuiSettingsUsername %></label>
<div class="col-md-7">
<div class="input-group">
<input type="text" class="form-control" id="username" name="username" autocomplete="username" value="admin" disabled>
</div>
</div>
</div>
<div class="row mb-1">
<label class="col-md-5 form-label" for="password"><%= $tWebuiSettingsPassword %></label>
<div class="col-md-7">
<div class="input-group">
<input type="password" class="form-control password" name="password" id="password" autocomplete="new-password" value="" placeholder="K3wLHaZk3R!">
<div class="input-group-text">
<input type="checkbox" class="toggle-password" tabindex="-1" title="<%= $tFormShowPasswordTitle %>">
</div>
</div>
</div>
</div>
<div class="row mb-1">
<label class="col-md-5 form-label" for="password"><%= $tWebuiSettingsPasswordConfirmation %></label>
<div class="col-md-7">
<div class="input-group">
<input type="password" class="form-control password" name="passwordconfirmation" id="passwordconfirmation" autocomplete="new-password" value="" placeholder="K3wLHaZk3R!">
<div class="input-group-text">
<input type="checkbox" class="toggle-password" tabindex="-1" title="<%= $tFormShowPasswordTitle %>">
</div>
</div>
</div>
</div>
<div class="row mb-1">
<label class="col-md-5 form-label" for="language"><%= $tWebuiSettingsLanguage %></label>
<div class="col-md-7">
<select class="form-select" name="language" id="language"><% for i in locale/*.sh; do
code=$(echo $i | sed 's#^locale/\(.*\)\.sh#\1#')
name=$(sed -n 2p $i | cut -d: -f2)
[ "$code" = "$locale" ] && selected=" selected" || selected=""
echo -n "<option value=\"${code}\"${selected}>${name}</option>"
done %></select>
</div>
</div>
<button type="submit" class="btn btn-primary"><%= $tButtonFormSubmit %></button>
</form>
</div>
</div>
</div>
</div>
<script src="/js/webui-password.js"></script>
<%in _footer.cgi %>
