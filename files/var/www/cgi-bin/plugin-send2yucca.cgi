#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="yucca"
plugin_name="Notify Yucca"
page_title="Notify Yucca"
params="enabled address host port"

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
  if [ "true" = "$email_enabled" ]; then
    [ -z "$yucca_host"    ] && flash_append "danger" "Yucca host cannot be empty." && error=11
    [ -z "$yucca_port"    ] && flash_append "danger" "Yucca port cannot be empty." && error=12
    [ -z "$yucca_address" ] && flash_append "danger" "Yucca address cannot be empty." && error=13
  fi

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
  [ -z "$yucca_port" ] && yucca_port="1025"
fi
%>
<%in p/header.cgi %>

<form action="<%= $SCRIPT_NAME %>" method="post">
  <% field_switch "yucca_enabled" "Enable notification to Yucca NVR" %>
  <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
    <div class="col">
      <% field_text "yucca_host" "Yucca host" %>
      <% field_text "yucca_port" "Yucca port" %>
      <% field_text "yucca_address" "Yucca address" %>
      <% # field_switch "email_socks5_enabled" "Use SOCKS5" "<a href=\"network-socks5.cgi\">Configure</a> SOCKS5 access" %>
      <% button_submit %>
    </div>
  </form>
  <div class="col">
    <% ex "cat $config_file" %>
  </div>
  <div class="col">
    <% preview %>
    <% if [ "true" = "$yucca_enabled" ]; then %>
      <p><a href="#" class="btn btn-primary" id="send-to-yucca">Send to Yucca</a></p>
    <% fi %>
  </div>
</div>

<%in p/footer.cgi %>
