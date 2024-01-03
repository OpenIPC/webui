#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="openwall"
plugin_name="Send to OpenWall"
page_title="Send to OpenWall"
params="caption enabled interval use_heif socks5_enabled"

tmp_file=/tmp/${plugin}.conf

config_file="${ui_config_dir}/${plugin}.conf"
[ ! -f "$config_file" ] && touch $config_file

if [ "POST" = "$REQUEST_METHOD" ]; then
	# parse values from parameters
	for p in $params; do
		eval ${plugin}_${p}=\$POST_${plugin}_${p}
		sanitize "${plugin}_${p}"
	done; unset p

	### Validation
	if [ "true" = "$openwall_enabled" ]; then
		[ "$openwall_interval" -lt "15" ] && set_error_flag "Keep interval at 15 minutes or longer."
	fi

	if [ -z "$error" ]; then
		# create temp config file
		:>$tmp_file
		for p in $params; do
			echo "${plugin}_${p}=\"$(eval echo \$${plugin}_${p})\"" >>$tmp_file
		done; unset p
		mv $tmp_file $config_file

		# Disable/enable cron job
		cp /etc/crontabs/root /tmp/crontabs.tmp
		sed -i /send2openwall\.sh/d /tmp/crontabs.tmp
		[ "true" = "$openwall_enabled" ] &&
		echo "*/${openwall_interval} * * * * /usr/sbin/send2openwall.sh" >>/tmp/crontabs.tmp
		mv /tmp/crontabs.tmp /etc/crontabs/root

		update_caminfo
		redirect_back "success" "${plugin_name} config updated."
	  fi

	redirect_to $SCRIPT_NAME
else
	include $config_file

	# Default values
	[ -z "$openwall_interval" ] && openwall_interval="15"
	[ -z "$openwall_use_heif" ] && openwall_use_heif="false"
fi
%>
<%in p/header.cgi %>

<div class="alert alert-info">
<p>This plugin allows you to share images from your OpenIPC camera on the <a href="https://openipc.org/open-wall">Open Wall</a>
 page of our website. But that's not all. It's a metrics agent with meaning. The images you share will allow us to determine
 the quality of images from different cameras. We also collect your MAC address, SoC model, sensor model, flash chip size,
 firmware version, and camera uptime to do this.</p>
</div>

<form action="<%= $SCRIPT_NAME %>" method="post">
  <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
    <div class="col">
      <% field_switch "openwall_enabled" "Enable sending to OpenWall" %>
      <% field_select "openwall_interval" "Interval, minutes" "15,30,60" "Time between submissions. 15 minutes or longer." %>
      <% field_text "openwall_caption" "Caption" "Location or short description." %>
      <% field_switch "openwall_use_heif" "Use HEIF format." "Requires H.265 codec on Video0." %>
      <% field_switch "openwall_socks5_enabled" "Use SOCKS5" "<a href=\"network-socks5.cgi\">Configure</a> SOCKS5 access." %>
    </div>
    <div class="col">
      <% ex "cat $config_file" %>
    </div>
    <div class="col">
      <% ex "grep send2openwall /etc/crontabs/root" %>
      <% button_webui_log %>
    </div>
  </div>
  <% button_submit %>
</form>

<% if [ "h265" != "$(yaml-cli -g .video0.codec)" ]; then %>
<script>
$('#openwall_use_heif').checked = false;
$('#openwall_use_heif').disabled = true;
</script>
<% fi %>

<%in p/footer.cgi %>
