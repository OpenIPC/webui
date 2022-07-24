#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="email"
plugin_name="Send to email"
page_title="Send to email"
params="enabled from_name from_address to_name to_address subject body smtp_server smtp_port smtp_login smtp_password socks5_enabled"

tmp_file=/tmp/${plugin}.conf
config_file="${ui_config_dir}/${plugin}.conf"
[ ! -f "$config_file" ] && touch $config_file

if [ "POST" = "$REQUEST_METHOD" ]; then
  # parse values from parameters
  for _p in $params; do
    eval ${plugin}_${_p}=\$POST_${plugin}_${_p}
    sanitize "${plugin}_${_p}"
  done; unset _p

  ### Normalization
  email_body="$(echo "$email_body" | tr "\r?\n" " ")"

  ### Validation
  if [ "true" = "$email_enabled" ]; then
    [ -z "$email_smtp_server"  ] && flash_append "danger" "SMTP server address cannot be empty." && error=1
    [ -z "$email_from_address" ] && flash_append "danger" "Sender email address cannot be empty." && error=1
    [ -z "$email_from_name"    ] && flash_append "danger" "Sender name cannot be empty." && error=1
    [ -z "$email_to_address"   ] && flash_append "danger" "Recipient email address cannot be empty." && error=1
    [ -z "$email_to_name"      ] && flash_append "danger" "Recipient name cannot be empty." && error=1
  fi

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

  # Default values
  [ -z "$email_smtp_port" ] && email_smtp_port="25"
  [ -z "$email_from_name" ] && email_from_name="Camera ${network_hostname}"
  [ -z "$email_to_name" ] && email_to_name="Camera admin"
  [ -z "$email_subject" ] && email_subject="Snapshot from ${network_hostname}"
fi
%>
<%in p/header.cgi %>

<form action="<%= $SCRIPT_NAME %>" method="post">
  <% field_switch "email_enabled" "Enable sending to email" %>
  <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
    <div class="col">
      <% field_text "email_smtp_server" "SMTP server" %>
      <% field_text "email_smtp_port" "SMTP port" %>
      <% field_text "email_smtp_login" "SMTP server login" %>
      <% field_password "email_smtp_password" "SMTP server password" %>
      <% field_text "email_from_name" "Email from name" %>
      <% field_text "email_from_address" "Email from address" "Use an email address where bounce reports can be sent to." %>
      <% field_text "email_to_name" "Email to name" %>
      <% field_text "email_to_address" "Email to address" %>
      <% field_text "email_subject" "Email subject" %>
      <% field_textarea "email_body" "Email body" "Line breaks will be replaced with whitespace." %>
      <% # field_switch "email_socks5_enabled" "Use SOCKS5" "<a href=\"network-socks5.cgi\">Configure</a> SOCKS5 access" %>
      <% button_submit %>
    </div>
  </form>
  <div class="col">
    <h3>Config file</h3>
    <% ex "cat $config_file" %>
  </div>
  <div class="col">
    <h3>Preview</h3>
    <p><img src="http://<%= $network_address %>/image.jpg" alt="Image: preview" class="img-fluid mb-3" id="preview-jpeg" width="1280" height="720"></p>
    <% if [ "true" = "$email_enabled" ]; then %>
      <p><a href="#" class="btn btn-primary" id="send-to-email">Send to email</a></p>
    <% fi %>
  </div>
</div>

<script>
$('#email_body').style.height = "6rem";
async function updatePreview() {
  await sleep(1000);
  $('#preview-jpeg').src = "http://<%= $network_address %>/image.jpg?t=" + Date.now();
}
$('#preview-jpeg').addEventListener('load', updatePreview);
updatePreview();
</script>

<%in p/footer.cgi %>
