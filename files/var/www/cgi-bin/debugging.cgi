#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="coredump"
page_title="Majestic debugging"
params="consent enabled ftphost ftppath ftppass ftpuser localpath save4web send2devs send2ftp send2tftp tftphost"

[ ! -f "/rom/${mj_bin_file}" ] && redirect_to "status.cgi" "danger" "Majestic is not supported on this system."

tmp_file=/tmp/${plugin}.conf
config_file=/etc/${plugin}.conf
[ ! -f "$config_file" ] && touch $config_file

# convert old config format
old_config_file=/etc/coredump.config
if [ -f $old_config_file ]; then
  mv $old_config_file $tmp_file
  if [ -f "$(wc -l $tmp_file | cut -d " " -f 1)" = "2" ]; then
    sed -i "/contact_/d" $tmp_file
    sed -i "s/^/coredump_/" $tmp_file
    sed -i "s/savedumps/enabled/" $tmp_file
    sed -i "s/haveconsent/consent/" $tmp_file
  fi
  mv $tmp_file $config_file
  flash_save "success" "Configuration file converted to new format."
fi
unset old_config_file

if [ "POST" = "$REQUEST_METHOD" ]; then
  # parse values from parameters
  for _p in $params; do
    eval ${plugin}_${_p}=\$POST_${plugin}_${_p}
    sanitize "${plugin}_${_p}"
  done; unset _p

  ### Normalization
  # FIXME: strip trailing slashes
  #sanitize "coredump_localpath"
  #sanitize "coredump_ftppath"

  ### Validation

  if [ "true" = "$coredump_enabled" ]; then
    if [ "true" = "$coredump_send2devs" ]; then
      [ -z "$admin_name" ] || [ -z "$admin_email" ] && flash_append "danger" "Please <a href=\"admin.cgi\">fill out the admin profile</a> first." && error=1
    fi
    [ "true" != "$coredump_consent"  ] && flash_append "danger" "You have to understand and acknowledge security risk." && error=1
    [ "true" = "$coredump_send2ftp"  ] && [ -z "$coredump_ftphost"   ] && flash_append "danger" "FTP address cannot be empty." && error=1
    [ "true" = "$coredump_send2tftp" ] && [ -z "$coredump_tftphost"  ] && flash_append "danger" "TFTP address cannot be empty." && error=1
    [ "true" = "$coredump_save4web"  ] && [ -z "$coredump_localpath" ] && flash_append "danger" "Local path cannot be empty." && error=1
  fi

  if [ -z "$error" ]; then
    # create temp config file
    :> $tmp_file
    for _p in $params; do
      echo "${plugin}_${_p}=\"$(eval echo \$${plugin}_${_p})\"" >> $tmp_file
    done; unset _p
    mv $tmp_file $config_file

    update_caminfo
    redirect_back "success" "Majestic debugging config updated."
  fi
else
  include $config_file
fi

[ -z "$coredump_ftpuser" ] && coredump_ftpuser="anonymous"
[ -z "$coredump_ftppass" ] && coredump_ftppass="anonymous"

if [ -z "$coredump_localpath" ]; then
  if [ -d "/mnt/mmc" ]; then
    coredump_localpath="/mnt/mmc"
  else
    coredump_localpath="/root"
  fi
fi
%>
<%in p/header.cgi %>

<% if [ -z "$(grep sendcoredump.sh /etc/init.d/S95*)" ]; then %>
  <div class="alert alert-warning">
    <p><b>This service requires a slight modification of /etc/init.d/S95... file.</b></p>
    <p>Please insert the following code inside <code>load_majestic()</code> block, right before <code>start-stop-daemon</code> line:</p>
    <pre class="bg-light p-3 text-black">
if [ -f $config_file ] && [ "true" = "$(grep ^savedumps $config_file | cut -d= -f2)" ]; then
  ulimit -c unlimited && echo "| /usr/sbin/sendcoredump.sh" > /proc/sys/kernel/core_pattern
fi
</pre>
  </div>
<% fi %>

<form action="<%= $SCRIPT_NAME %>" method="post">
  <div class="row row-cols-1 row-cols-md-2 row-cols-xl-3 row-cols-xxl-4 g-4">
    <div class="col">
      <h3>Core dump saving</h3>
      <% field_switch "coredump_enabled" "Enable core dump saving" %>
    </div>
    <div class="col">
      <h3>Upload to AWS S3 bucket</h3>
      <% field_switch "coredump_send2devs" "Upload to developers" %>
      <% field_checkbox "coredump_consent" "I am aware of sensitive information in core dumps and I trust the developers" %>
    </div>
    <div class="col">
      <h3>Leave on camera</h3>
      <% field_switch "coredump_save4web" "Save file on camera" "Not recommended!" %>
      <% field_text "coredump_localpath" "Local path" %>
<% if [ -f "${coredump_localpath}/coredump.tgz" ]; then %>
      <div class="alert alert-danger">
        <h5>There is a core dump saved on the camera!</h5>
        <p class="mb-0">Please retrieve and delete file /root/coredump.tgz from the camera.</h5>
      </div>
<% fi %>
    </div>
    <div class="col">
      <h3>Upload to TFTP server</h3>
      <% field_switch "coredump_send2tftp" "Upload to TFTP server" %>
      <% field_text "coredump_tftphost" "Host" "FQDN or IP address" %>
    </div>
    <div class="col">
      <h3>Upload to FTP server</h3>
      <% field_switch "coredump_send2ftp" "Upload to FTP server" %>
      <% field_text "coredump_ftphost" "Host" "FQDN or IP address" %>
      <% field_text "coredump_ftppath" "Target directory" "relative to ftp root directory" %>
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

<button type="button" class="btn btn-info" data-bs-toggle="modal" data-bs-target="#helpModal">How is works?</button>

<%in p/footer.cgi %>
