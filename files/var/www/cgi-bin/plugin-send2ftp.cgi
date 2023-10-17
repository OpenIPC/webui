#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="ftp"
plugin_name="Send to FTP"
page_title="Send to FTP"
params="enabled host username password path port socks5_enabled template"

tmp_file=/tmp/${plugin}.conf

config_file="${ui_config_dir}/${plugin}.conf"
[ ! -f "$config_file" ] && touch $config_file

if [ "POST" = "$REQUEST_METHOD" ]; then
  # parse values from parameters
  for _p in $params; do
    eval ${plugin}_${_p}=\$POST_${plugin}_${_p}
    sanitize "${plugin}_${_p}"
  done; unset _p

  ### Validation
  if [ "true" = "$ftp_enabled" ]; then
    [ "true" = "$ftp_send2ftp"  ] && [ -z "$ftp_ftphost"   ] && flash_append "danger" "FTP address cannot be empty." && error=11
    [ "true" = "$ftp_send2tftp" ] && [ -z "$ftp_tftphost"  ] && flash_append "danger" "TFTP address cannot be empty." && error=12
    [ "true" = "$ftp_save4web"  ] && [ -z "$ftp_localpath" ] && flash_append "danger" "Local path cannot be empty." && error=13
  fi
  [ -z "$ftp_template" ] && ftp_template="Screenshot-%Y%m%d-%H%M%S.jpg"

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

  redirect_to $SCRIPT_NAME
else
  include $config_file

  # Default values
  [ -z "$ftp_port" ] && ftp_port="21"
  [ -z "$ftp_template" ] && ftp_template="${network_hostname}-%Y%m%d-%H%M%S.jpg"
fi
%>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_switch "ftp_enabled" "Enable sending to FTP server" %>
      <% field_text "ftp_host" "FTP host" %>
      <% field_text "ftp_port" "FTP port" %>
      <% field_text "ftp_username" "FTP username" %>
      <% field_password "ftp_password" "FTP password" %>
      <% field_text "ftp_path" "FTP path" "relative to FTP root directory" %>
      <% field_text "ftp_template" "File template" "Supports <a href=\"https://man7.org/linux/man-pages/man3/strftime.3.html \" target=\"_blank\">strftime()</a> format. Using subdirectories in template is alowed." %>
      <% field_switch "ftp_socks5_enabled" "Use SOCKS5" "<a href=\"network-socks5.cgi\">Configure</a> SOCKS5 access" %>
      <% button_submit %>
    </form>
  </div>
  <div class="col">
    <% ex "cat $config_file" %>
    <% button_webui_log %>
  </div>
</div>

<%in p/footer.cgi %>
