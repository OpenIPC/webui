#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="coredump"
plugin_name="Majestic debugging"
page_title="Majestic debugging"
params="consent enabled ftphost ftppath ftppass ftpuser localpath save4web send2devs send2ftp send2tftp tftphost"

[ ! -f "/rom/${mj_bin_file}" ] && redirect_to "status.cgi" "danger" $STR_NOT_SUPPORTED

tmp_file=/tmp/${plugin}.conf
config_file=/etc/${plugin}.conf
[ ! -f "$config_file" ] && touch $config_file

if [ "POST" = "$REQUEST_METHOD" ]; then
	# parse values from parameters
	for p in $params; do
		eval ${plugin}_${p}=\$POST_${plugin}_${p}
		sanitize "${plugin}_${p}"
	done; unset p

	### Normalization
	# FIXME: strip trailing slashes
	#sanitize "coredump_localpath"
	#sanitize "coredump_ftppath"

	### Validation
	if [ "true" = "$coredump_enabled" ]; then
		if [ "true" = "$coredump_send2devs" ]; then
			if [ -z "$admin_name" ] || [ -z "$admin_email" ]; then
				set_error_flag "Please <a href=\"admin.cgi\">fill out the admin profile</a> first."
			fi
		fi

		if [ "true" != "$coredump_consent" ]; then
			set_error_flag "You have to understand and acknowledge security risk."
		fi

		if [ "true" = "$coredump_send2ftp" ] && [ -z "$coredump_ftphost" ]; then
			set_error_flag "FTP address cannot be empty."
		fi

		if [ "true" = "$coredump_send2tftp" ] && [ -z "$coredump_tftphost" ]; then
			set_error_flag "TFTP address cannot be empty."
		fi

		if [ "true" = "$coredump_save4web"  ] && [ -z "$coredump_localpath" ]; then
			set_error_flag "Local path cannot be empty."
		fi
	fi

	if [ -z "$error" ]; then
		# create temp config file
		:>$tmp_file
		for p in $params; do
			echo "${plugin}_${p}=\"$(eval echo \$${plugin}_${p})\"" >>$tmp_file
		done; unset p
		mv $tmp_file $config_file

		update_caminfo
		touch /tmp/coredump-restart.txt
		redirect_back "success" "${plugin_name} config updated."
	fi
else
	include $config_file
fi

[ -z "$coredump_ftpuser" ] && coredump_ftpuser="anonymous"
[ -z "$coredump_ftppass" ] && coredump_ftppass="anonymous"
[ -z "$coredump_tftphost" ] && coredump_tftphost=$(fw_printenv -n serverip)

if [ -z "$coredump_localpath" ]; then
	if [ -d "/mnt/mmc" ]; then
		coredump_localpath="/mnt/mmc"
	else
		coredump_localpath="/root"
	fi
fi
%>
<%in p/header.cgi %>

<% if [ -z "$(grep coredump_enabled /etc/init.d/S95*)" ]; then %>
  <div class="alert alert-warning">
    <p><b>This service requires a slight modification of /etc/init.d/S95... file.</b></p>
    <p>Please insert or adjust the following code inside <code>load_majestic()</code> block, right before <code>start-stop-daemon</code> line:</p>
    <pre class="bg-light p-3 text-black">
[ -f /etc/coredump.conf ] && . /etc/coredump.conf
if [ "$coredump_enabled" ]; then
  [ "$(yaml-cli -i /etc/majestic.yaml -g .watchdog.timeout)" -lt "30" ] && yaml-cli -i /etc/majestic.yaml -s .watchdog.timeout 30
  ulimit -c unlimited && echo "|/usr/sbin/sendcoredump.sh" >/proc/sys/kernel/core_pattern
fi
</pre>
  </div>
<% fi %>

<% if [ "true" = "$(yaml-cli -g .watchdog.enabled)" ] && [ "$(yaml-cli -g .watchdog.timeout)" -le 60 ]; then %>
<div class="alert alert-warning">
<p class="mb-0">Please disable watchdog or <a href="majestic-settings.cgi?tab=watchdog">change its timeout value</a> to 60 seconds or more.
Shorter timeout may affect coredump saving.</p>
</div>
<% fi %>

<form action="<%= $SCRIPT_NAME %>" method="post">
  <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
    <div class="col">
      <h3>Core dump saving</h3>
      <% field_switch "coredump_enabled" "Enable core dump saving" %>
      <% field_switch "coredump_send2devs" "Upload core dump to developers" %>
      <% field_checkbox "coredump_consent" "I am aware of sensitive information in core dumps and I trust the developers" %>

      <button type="button" class="btn btn-info my-3" data-bs-toggle="modal" data-bs-target="#helpModal">How does it work?</button>
    </div>
    <div class="col">
      <h3>Save on camera</h3>
      <% field_switch "coredump_save4web" "Enable saving on camera" "Not recommended unless you save to an SD card!" %>
      <% field_text "coredump_localpath" "Save to local directory" %>
<% if [ -f "${coredump_localpath}/coredump.tgz" ]; then %>
      <div class="alert alert-danger">
        <h5>There is a core dump saved on the camera!</h5>
        <p class="mb-0">Please retrieve and delete file /root/coredump.tgz from the camera.</h5>
      </div>
<% fi %>
      <h3>Upload to TFTP server</h3>
      <% field_switch "coredump_send2tftp" "Enable uploading to TFTP server" %>
      <% field_text "coredump_tftphost" "TFTP server host" "FQDN or IP address" %>
    </div>
    <div class="col">
      <h3>Upload to FTP server</h3>
      <% field_switch "coredump_send2ftp" "Enable uploading to FTP server" %>
      <% field_text "coredump_ftphost" "FTP server host" "FQDN or IP address" %>
      <% field_text "coredump_ftppath" "Save to FTP directory" "relative to FTP root directory" %>
      <% field_text "coredump_ftpuser" "Username" %>
      <% field_password "coredump_ftppass" "Password" %>
    </div>
    <div class="col">
      <h3>Config</h3>
      <% [ -f "$config_file" ] && ex "cat $config_file" %>
    </div>
    <div class="col">
      <h3>Log of last core dumping</h3>
      <% [ -f /root/coredump.log ] && ex "cat /root/coredump.log" %>
    </div>
  </div>
  <% button_submit %>
</form>

<div class="modal fade" id="helpModal" tabindex="-1" aria-labelledby="helpModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">How it works</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <p>Core dump is the contents of random access memory (RAM) at the moment of program crashing. Core dump is taken for the purpose of debugging the program. Core dump is bundled along with the system information and your contact information, and gets uploaded directly to developers' remote server.</p>
        <p>Please be aware that core dumps may contain sensitive information like passwords and security keys. If you don't fill comfortable sharing such kind of data, please don't enable saving core dumps.</p>
        <p>If your camera does not have direct access to the internet, you can set up uploading of the bundle to an FTP or TFTP server on your local network, so that you could retrieve it and send to the developers. Please make sure that your FTP/TFTP server can accept incoming files.</p>
        <p class="mb-0">If you do not have an FTP/TFTP server in your local network to save the dumped core on, you can opt to save it directly on camera to retrieve later. You are strongly advised against doing that if any other option is feasable. Saving bundle on camera can exhaust free space and render camera unstable or unusable.</p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>

<%in p/footer.cgi %>
