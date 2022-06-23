#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="$t_mjdebug_0"

if [ ! -f "/rom/${mj_bin_file}" ]; then
  flash_save "danger" "$t_mjdebug_1"
  redirect_to "/cgi-bin/status.cgi"
fi

conf_file=/etc/coredump.config

if [ "POST" = "$REQUEST_METHOD" ]; then
  ### Assigning values
  coredump_savedumps="$POST_coredump_enabled"
  coredump_haveconsent="$POST_coredump_consent"
  coredump_send2devs="$POST_coredump_send2devs"
  coredump_contact_name="$POST_coredump_name"
  coredump_contact_email="$POST_coredump_email"
  coredump_contact_telegram="$POST_coredump_telegram"
  coredump_send2tftp="$POST_coredump_send2tftp"
  coredump_tftphost="$POST_coredump_tftphost"
  coredump_send2ftp="$POST_coredump_send2ftp"
  coredump_ftphost="$POST_coredump_ftphost"
  coredump_ftppath="$POST_coredump_ftppath"
  coredump_ftpuser="$POST_coredump_ftpuser"
  coredump_ftppass="$POST_coredump_ftppass"
  coredump_save4web="$POST_coredump_save4web"
  coredump_localpath="$POST_coredump_localpath"

  ### Normalization
  # strip trailing slashes
  sanitize "coredump_localpath"
  sanitize "coredump_ftppath"

  ### Validation
  if [ "$coredump_savedumps" = "true" ]; then
    if [ ! "$coredump_haveconsent" = "true" ]; then
      error="$t_form_error_6"
    else
      if [ "$coredump_send2tftp" = "true" ]; then
        [ -z "$coredump_tftphost" ] && error="$t_form_error_7"
      fi
      if [ "$coredump_save4web" = "true" ]; then
        [ -z "$coredump_localpath" ] && error="$t_form_error_8"
      fi
    fi
  fi

  if [ -z "$error" ]; then
    echo "# /etc/coredump.config
savedumps=${coredump_savedumps}
haveconsent=${coredump_haveconsent}
contact_name=${coredump_contact_name}
contact_email=${coredump_contact_email}
contact_telegram=${coredump_contact_telegram}
send2devs=${coredump_send2devs}
send2tftp=${coredump_send2tftp}
tftphost=${coredump_tftphost}
send2ftp=${coredump_send2ftp}
ftphost=${coredump_ftphost}
ftppath=${coredump_ftppath}
ftpuser=${coredump_ftpuser}
ftppass=${coredump_ftppass}
save4web=${coredump_save4web}
localpath=${coredump_localpath}
" > /etc/coredump.config
    flash_save "success" "$t_mjdebug_2"
    redirect_to "/cgi-bin/majestic-debug.cgi"
  fi
else
  coredump_enabled=$(grep ^savedumps $conf_file | cut -d= -f2)
  coredump_consent=$(grep ^haveconsent $conf_file | cut -d= -f2)
  coredump_name=$(grep ^contact_name $conf_file | cut -d= -f2)
  coredump_email=$(grep ^contact_email $conf_file | cut -d= -f2)
  coredump_telegram=$(grep ^contact_telegram $conf_file | cut -d= -f2)
  coredump_send2devs=$(grep ^send2devs $conf_file | cut -d= -f2)
  coredump_send2tftp=$(grep ^send2tftp $conf_file | cut -d= -f2)
  coredump_tftphost=$(grep ^tftphost $conf_file | cut -d= -f2)
  coredump_send2ftp=$(grep ^send2ftp $conf_file | cut -d= -f2)
  coredump_ftphost=$(grep ^ftphost $conf_file | cut -d= -f2)
  coredump_ftppath=$(grep ^ftppath $conf_file | cut -d= -f2)
  coredump_ftpuser=$(grep ^ftpuser $conf_file | cut -d= -f2)
  coredump_ftppass=$(grep ^ftppass $conf_file | cut -d= -f2)
  coredump_save4web=$(grep ^save4web $conf_file | cut -d= -f2)
  coredump_localpath=$(grep ^localpath $conf_file | cut -d= -f2)
  if [ -z "$coredump_localpath" ]; then
    if [ -d "/mnt/mmc" ]; then
      coredump_localpath="/mnt/mmc"
    else
      coredump_localpath="/root"
    fi
  fi
fi
%>
<%in p/header.cgi %>
<%
if [ -n "$error" ]; then
  report_error "$error"
fi

if [ -z "$(grep sendcoredump.sh /etc/init.d/S95*)" ]; then
%>
<div class="alert alert-warning">
<p><b><%= $t_mjdebug_3 %></b></p>
<p><%= $t_mjdebug_4 %></p>
<pre class="bg-light p-3 text-black">
if [ $(grep ^savedumps /etc/coredump.config | cut -d= -f2) == "true" ]; then
  ulimit -c unlimited && echo "| /usr/sbin/sendcoredump.sh" > /proc/sys/kernel/core_pattern
fi
</pre>
</div>
<% fi %>
<form action="/cgi-bin/majestic-debug.cgi" method="post">
<div class="row row-cols-1 row-cols-lg-2 row-cols-xl-3 g-4">
<div class="col">
<h3><% $t_mjdebug_5 %></h3>
<% [ -f /root/coredump.log ] && ex "cat /root/coredump.log" %>
<h3><%= $t_mjdebug_6 %></h3>
<%
field_switch "coredump_enabled"
field_text "coredump_name"
field_text "coredump_email"
field_text "coredump_telegram"
field_switch "coredump_consent"
%>
<h3><%= $t_mjdebug_7 %></h3>
<%
field_switch "coredump_send2devs"
%>
</div>
<div class="col">
<h3><%= $t_mjdebug_8 %></h3>
<%
field_switch "coredump_send2tftp"
field_text "coredump_tftphost"
%>
<h3><%= $t_mjdebug_8 %></h3>
<%
field_switch "coredump_send2ftp"
field_text "coredump_ftphost"
field_text "coredump_ftppath"
field_text "coredump_ftpuser"
field_password "coredump_ftppass"
%>
<h3><%= $t_mjdebug_a %></h3>
<%
field_switch "coredump_save4web"
field_text "coredump_localpath"
if [ -f "${coredump_localpath}/coredump.tgz" ]; then
%>
<div class="alert alert-danger">
<h5><%= $t_mjdebug_b %></h5>
<p class="mb-0"><%= $t_mjdebug_c %></h5>
</div>
<% fi %>
</div>
<div class="col">
<div class="alert alert-info">
<h3><%= $t_mjdebug_c %></h3>
<p><%= $t_mjdebug_d %></p>
<p><%= $t_mjdebug_e %></p>
<p><%= $t_mjdebug_f %></p>
<p class="mb-0"><%= $t_mjdebug_g %></p>
</div>
</div>
</div>
<% button_submit %>
</form>
<%in p/footer.cgi %>
