#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleMajesticDebug"

get_software_info
if [ ! -f /rom/${mj_bin_file} ]; then
  flash_save "danger" "$tMsgMajesticIsNotSupported"
  redirect_to "/cgi-bin/status.cgi"
fi

conf_file=/etc/coredump.config
# [ ! -f "$conf_file" ] && error="$tMjDebugErrorConfigNotFound"

if [ "$REQUEST_METHOD" == "POST" ]; then
  savedumps="$POST_coredump_enabled"
  haveconsent="$POST_coredump_consent"
  send2devs="$POST_coredump_send2devs"
  contact_name="$POST_coredump_name"
  contact_email="$POST_coredump_email"
  contact_telegram="$POST_coredump_telegram"
  send2tftp="$POST_coredump_send2tftp"
  tftphost="$POST_coredump_tftphost"

  if [ "$savedumps" == "true" ]; then
    if [ ! "$haveconsent" == "true" ]; then
      error="$tMjDebugErrorConsent"
    else
      if [ "$send2tftp" == "true" ]; then
        if [ -z "$tftphost" ]; then
          error="$tMjDebugErrorTftpHostEmpty"
        fi
      fi
    fi
  fi

  if [ -n "$error" ]; then
    flash_save "danger" "$error"
  else
    echo "# /etc/coredump.config
contact_name=${contact_name}
contact_email=${contact_email}
contact_telegram=${contact_telegram}
haveconsent=${haveconsent}
send2devs=${send2devs}
send2tftp=${send2tftp}
tftphost=${tftphost}
savedumps=${savedumps}
" > /etc/coredump.config
    flash_save "success" "$tMjDebugConfigUpdated"
    redirect_to "/cgi-bin/majestic-debug.cgi"
  fi
fi

coredump_enabled=$(grep savedumps $conf_file | cut -d= -f2)
coredump_consent=$(grep haveconsent $conf_file | cut -d= -f2)
coredump_name=$(grep contact_name $conf_file | cut -d= -f2)
coredump_email=$(grep contact_email $conf_file | cut -d= -f2)
coredump_telegram=$(grep contact_telegram $conf_file | cut -d= -f2)
coredump_send2tftp=$(grep send2tftp $conf_file | cut -d= -f2)
coredump_send2devs=$(grep send2devs $conf_file | cut -d= -f2)
coredump_tftphost=$(grep tftphost $conf_file | cut -d= -f2)
%>
<%in _header.cgi %>
<%
if [ -n "$error" ]; then
  report_error "$error"
  report_log "$log"
else
%>
<form action="/cgi-bin/majestic-debug.cgi" method="post">
  <div class="row row-cols-1 row-cols-xl-2 g-4 mb-4">
    <div class="col">
      <div class="card mb-3">
        <h5 class="card-header"><%= $tHeaderMjDebug %></h5>
        <div class="card-body">
          <% field_switch "coredump_enabled" %>
          <% field_checkbox "coredump_consent" %>
        </div>
      </div>
      <div class="card mb-3">
        <h5 class="card-header"><%= $tHeaderMjDebugUploadS3 %></h5>
        <div class="card-body">
          <% field_switch "coredump_send2devs" %>
        </div>
      </div>
      <div class="card mb-3">
        <h5 class="card-header"><%= $tHeaderMjDebugStorage %></h5>
        <div class="card-body">
          <% field_switch "coredump_send2tftp" %>
          <% field_text "coredump_tftphost" %>
        </div>
      </div>
      <div class="card mb-3">
        <h5 class="card-header"><%= $tHeaderMjDebugContactInfo %></h5>
        <div class="card-body">
          <% field_text "coredump_name" %>
          <% field_text "coredump_email" %>
          <% field_text "coredump_telegram" %>
        </div>
      </div>
      <% button_submit %>
    </div>
    <div class="col">
      <div class="alert alert-info">
        <%= $tMjDebugDescription %>
      </div>
    </div>
  </div>
</form>
<% fi %>
<%in _footer.cgi %>
