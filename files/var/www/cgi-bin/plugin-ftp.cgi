#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="ftp"
plugin_name="FTP Storage"
page_title="FTP Storage"
params="enabled template host login password path socks5_enabled"

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
    [ "true" = "$ftp_send2ftp"  ] && [ -z "$ftp_ftphost"   ] && flash_append "danger" "FTP address cannot be empty." && error=1
    [ "true" = "$ftp_send2tftp" ] && [ -z "$ftp_tftphost"  ] && flash_append "danger" "TFTP address cannot be empty." && error=1
    [ "true" = "$ftp_save4web"  ] && [ -z "$ftp_localpath" ] && flash_append "danger" "Local path cannot be empty." && error=1
  fi
  [ -z "$ftp_template" ] && ftp_template="Screenshot-%Y%m%d-%H%M%S.jpg"

  if [ -z "$error" ]; then
    # create temp config file
    :> $tmp_file
    for _p in $params; do
      echo "${plugin}_${_p}=\"$(eval echo \$${plugin}_${_p})\"" >> $tmp_file
    done; unset _p
    mv $tmp_file $config_file

    update_caminfo
    redirect_back "success" "${plugin_name} config updated."
  fi

  redirect_to $SCRIPT_NAME
else
  include $config_file
fi
%>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <h3>FTP Storage</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_switch "ftp_enabled" "Enable FTP Storage" %>
      <% field_text "ftp_template" "File template" "Supports <a href=\"https://man7.org/linux/man-pages/man3/strftime.3.html \" target=\"_blank\">strftime()</a> format." %>
      <% field_text "ftp_host" "FTP Storage host" %>
      <% field_text "ftp_login" "FTP Storage login" %>
      <% field_password "ftp_password" "FTP Storage password" %>
      <% field_text "ftp_path" "FTP Storage path" "relative to FTP root directory" %>
      <% field_switch "ftp_socks5_enabled" "Use SOCKS5" "<a href=\"network-socks5.cgi\">Configure</a> SOCKS5 access" %>
      <% button_submit %>
    </form>
  </div>
  <div class="col">
    <h3>Config file</h3>
    <% ex "cat $config_file" %>
  </div>
  <div class="col">
    <h3>Preview</h3>
    <p><img src="http://<%= $network_address %>/image.jpg" alt="Image: preview" class="img-fluid mb-3" id="preview-jpeg" width="1280" height="720"></p>
    <% if [ -n "$ftp_login" ] && [ -n "$ftp_password" ]; then %>
      <p><a href="#" class="btn btn-primary" id="send-to-ftp">Send to FTP Storage</a></p>
    <% fi %>
  </div>
</div>

<script>
async function updatePreview() {
  await sleep(1000);
  $('#preview-jpeg').src = "http://<%= $network_address %>/image.jpg?t=" + Date.now();
}
$('#preview-jpeg').addEventListener('load', updatePreview);
updatePreview();
</script>

<%in p/footer.cgi %>
