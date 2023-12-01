#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="webhook"
plugin_name="Send to Webhook"
page_title="Send to Webhook"
params="enabled attach_snapshot use_heif url socks5_enabled"

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
	if [ "true" = "$webhook_enabled" ]; then
		[ -z "$webhook_url"   ] && flash_append "danger" "Webhook URL cannot be empty." && error=11
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

	[ -z "$webhook_attach_snapshot" ] && webhook_attach_snapshot="true"
	[ -z "$webhook_use_heif" ] && webhook_use_heif="false"
fi
%>
<%in p/header.cgi %>

<form action="<%= $SCRIPT_NAME %>" method="post">
  <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
    <div class="col">
      <% field_switch "webhook_enabled" "Enable sending to webhook" %>
      <% field_text "webhook_url" "Webhook URL" %>
      <% field_switch "webhook_attach_snapshot" "Attach Snapshot" %>
      <% field_switch "webhook_use_heif" "Use HEIF format." "Requires H.265 codec on Video0." %>
      <% field_switch "webhook_socks5_enabled" "Use SOCKS5" "<a href=\"network-socks5.cgi\">Configure</a> SOCKS5 access" %>
    </div>
    <div class="col">
      <% ex "cat $config_file" %>
      <% button_webui_log %>
    </div>
  </div>
  <% button_submit %>
</form>

<%in p/footer.cgi %>
