#!/usr/bin/haserl
<%in _common.cgi %>
<%
plugin="vtun"
page_title="$tPageTitlePluginVtun"
service_file=/etc/init.d/S98vtun

if [ -n "$POST_action" ] && [ "$POST_action" = "reset" ]; then
  killall tunnel
  killall vtund
  rm ${service_file}
  redirect_to "/cgi-bin/plugin-vtun.cgi"
fi

if [ -n "$POST_server" ]; then
  echo -e "#!/bin/sh\n\ntunnel $POST_server" > ${service_file}
  chmod +x ${service_file}
  ${service_file}
  redirect_to "/cgi-bin/plugin-vtun.cgi"
fi
%>
<%in _header.cgi %>
<div class="row">
  <div class="col-md-6 mb-3">
    <div class="card">
      <div class="card-header"><%= $tHeaderVtun %></div>
      <div class="card-body">
        <form action="/cgi-bin/plugin-vtun.cgi" method="post">
          <% if [ -f "$service_file" ]; then %>
            <b><%= $service_file %></b>
            <pre><% echo "$(cat $service_file)" %></pre>
            <button type="submit" class="btn btn-danger" data-method="delete" name="action" value="reset"><%= $tButtonResetConfig %></button>
          <% else %>
            <div class="row mb-3">
              <div class="col-2">
                <label class="form-label" for="server"><%= $tLabelVtunServer %></label>
              </div>
              <div class="col-auto">
                <input class="form-control" type="text" id="server" name="server" value="<%= $server %>" size="45"<% [ -n "$server" ] && echo -n " disabled" %>>
              </div>
              <div class="col-auto">
                <span id="tokenHelpBlock" class="form-text"><%= $tHintVtunServer %></span>
              </div>
            </div>
            <button type="submit" class="btn btn-primary"><%= $tButtonFormSubmit %></button>
          <% fi %>
        </form>
      </div>
    </div>
  </div>
</div>
<%in _footer.cgi %>
