#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="ntfy"
plugin_name="Send to NTFY"
page_title="Send to NTFY"
params="enabled attach_snapshot msg_title msg_body msg_priority url port topic username password"

tmp_file=/tmp/${plugin}.conf

config_file="${ui_config_dir}/${plugin}.conf"
[ ! -f "$config_file" ] && touch $config_file

if [ "POST" = "$REQUEST_METHOD" ]; then
	# parse values from parameters
	for p in $params; do
		eval ${plugin}_${p}=\$POST_${plugin}_${p}
		sanitize "${plugin}_${p}"
	done; unset p

	### Normalization
	msg_body="$(echo "$msg_body" | tr "\r?\n" " ")"

	### Validation
	if [ "true" = "$ntfy_enabled" ]; then
		[ -z "$ntfy_url"    ] && set_error_flag "Server URL cannot be empty."
		[ -z "$ntfy_port" ] && set_error_flag "Server port cannot be empty."
		[ -z "$ntfy_topic"    ] && set_error_flag "NTFY topic name cannot be empty."
	fi

	if [ -z "$error" ]; then
		# create temp config file
		:>$tmp_file
		for p in $params; do
			echo "${plugin}_${p}=\"$(eval echo \$${plugin}_${p})\"" >>$tmp_file
		done; unset p
		mv $tmp_file $config_file

		update_caminfo
		redirect_back "success" "${plugin_name} config updated."
	fi

	redirect_to $SCRIPT_NAME
else
	include $config_file

	# Default values
	[ -z "$ntfy_attach_snapshot" ] && ntfy_attach_snapshot="true"
	[ -z "$ntfy_port" ] && ntfy_port="80"
	[ -z "$ntfy_msg_title" ] && ntfy_msg_title="OpenIPC Notify"
	[ -z "$ntfy_msg_body" ] && ntfy_msg_body="Motion detected!\n Is it friend or foe?"
        [ -z "$ntfy_msg_priority" ] && ntfy_msg_priority="default"
fi
%>
<%in p/header.cgi %>

<form action="<%= $SCRIPT_NAME %>" method="post">
  <% field_switch "ntfy_enabled" "Enable sending notification" %>
  <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
    <div class="col">
      <% field_text "ntfy_url" "NTFY server URL (IP or domain)" "example: http://192.168.1.10 or https://ntfy.sh"%>
      <% field_number "ntfy_port" "Server port" %>
      <% field_text "ntfy_topic" "Topic" %>
      <% field_select "ntfy_msg_priority" "Priority" "min low default high urgent" %>
      <% field_text "ntfy_username" "NTFY username" %>
      <% field_password "ntfy_password" "NTFY password" %>
    </div>
    <div class="col">
      <% field_text "ntfy_msg_title" "Title" %>
      <% field_textarea "ntfy_msg_body" "Message text" "Line breaks will be replaced with whitespace. Use \n instead" %>
      <% field_switch "ntfy_attach_snapshot" "Attach snapshot" %>
    </div>
    <div class="col">
      <% ex "cat $config_file" %>
      <% button_webui_log %>
    </div>
  </div>
  <% button_submit %>
</form>

<%in p/footer.cgi %>
