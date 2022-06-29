#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Majestic debugging"

[ ! -f "/rom/${mj_bin_file}" ] && redirect_to "status.cgi" "danger" "Majestic is not supported on this system."

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
    flash_save "success" "Majestic debug config updated."
    redirect_to "majestic-debug.cgi"
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

<button type="button" class="btn btn-info" data-bs-toggle="modal" data-bs-target="#helpModal">How is works?</button>

<%
if [ -n "$error" ]; then
  report_error "$error"
fi

if [ -z "$(grep sendcoredump.sh /etc/init.d/S95*)" ]; then
%>
  <div class="alert alert-warning">
    <p><b>This service requires a slight modification of /etc/init.d/S95... file.</b></p>
    <p>Please insert the following code inside <code>load_majestic()</code> block, right before <code>start-stop-daemon</code> line:</p>
    <pre class="bg-light p-3 text-black">
if [ $(grep ^savedumps /etc/coredump.config | cut -d= -f2) == "true" ]; then
  ulimit -c unlimited && echo "| /usr/sbin/sendcoredump.sh" > /proc/sys/kernel/core_pattern
fi
</pre>
  </div>
<% fi %>

<form action="<%= $SCRIPT_NAME %>" method="post">
  <div class="row row-cols-1 row-cols-md-2 row-cols-xxl-5 g-4">
    <div class="col">
      <h3>Core dump saving</h3>
      <p class="boolean">
        <span class="form-check form-switch">
          <input type="hidden" name="coredump_enabled" id="coredump_enabled-false" value="false">
          <input type="checkbox" id="coredump_enabled" name="coredump_enabled" value="true" class="form-check-input" role="switch"<% [ "true" = "$coredump_enabled" ] && echo " checked" %>>
          <label for="coredump_enabled" class="form-label form-check-label">Enable core dump saving</label>
        </span>
      </p>
      <p class="string">
        <label for="coredump_name" class="form-label">Name</label>
        <input type="text" id="coredump_name" name="coredump_name" class="form-control" value="<%= $coredump_name %>">
      </p>
      <p class="string">
        <label for="coredump_email" class="form-label">Email address</label>
        <input type="text" id="coredump_email" name="coredump_email" class="form-control" value="<%= $coredump_email %>">
      </p>
      <p class="string">
        <label for="coredump_telegram" class="form-label">Telegram username</label>
        <input type="text" id="coredump_telegram" name="coredump_telegram" class="form-control" value="<%= $coredump_telegram %>">
      </p>
    </div>

    <div class="col">
      <h3>Upload to AWS S3 bucket</h3>
      <p class="boolean">
        <span class="form-check form-switch">
          <input type="hidden" name="coredump_send2devs" id="coredump_send2devs-false" value="false">
          <input type="checkbox" id="coredump_send2devs" name="coredump_send2devs" value="true" class="form-check-input" role="switch"<% [ "true" = "$coredump_send2devs" ] && echo " checked" %>>
          <label for="coredump_send2devs" class="form-label form-check-label">Upload to developers</label>
        </span>
      </p>
      <p class="boolean">
        <span class="form-check form-switch">
          <input type="hidden" name="coredump_consent" id="coredump_consent-false" value="false">
          <input type="checkbox" id="coredump_consent" name="coredump_consent" value="true" class="form-check-input" role="switch"<% [ "true" = "$coredump_consent"] && echo " checked" %>>
          <label for="coredump_consent" class="form-label form-check-label">I am aware of sensitive information in core dumps and I trust the developers.</label>
        </span>
      </p>
    </div>

    <div class="col">
      <h3>Leave on camera</h3>
      <p class="boolean">
        <span class="form-check form-switch">
          <input type="hidden" name="coredump_save4web" id="coredump_save4web-false" value="false">
          <input type="checkbox" id="coredump_save4web" name="coredump_save4web" value="true" class="form-check-input" role="switch"<% [ "true" = "$coredump_save4web" ] && echo " checked" %>>
          <label for="coredump_save4web" class="form-label form-check-label">Save file on camera</label>
        </span>
        <span class="hint text-secondary">Not recommended!</span>
      </p>
      <p class="string">
        <label for="coredump_localpath" class="form-label">Local path</label>
        <input type="text" id="coredump_localpath" name="coredump_localpath" value="<%= $coredump_localpath %>" class="form-control">
      </p>

<% if [ -f "${coredump_localpath}/coredump.tgz" ]; then %>
      <div class="alert alert-danger">
        <h5>There is a core dump saved on the camera!</h5>
        <p class="mb-0">Please retrieve and delete file /root/coredump.tgz from the camera.</h5>
      </div>
<% fi %>
    </div>

    <div class="col">
      <h3>Upload to TFTP server</h3>
      <p class="boolean">
        <span class="form-check form-switch">
          <input type="hidden" name="coredump_send2tftp" id="coredump_send2tftp-false" value="false">
          <input type="checkbox" id="coredump_send2tftp" name="coredump_send2tftp" value="true" class="form-check-input" role="switch"<% [ "true" = "$coredump_send2tftp" ] && echo " checked" %>>
          <label for="coredump_send2tftp" class="form-label form-check-label">Upload to TFTP server</label>
        </span>
      </p>
      <p class="string">
        <label for="coredump_tftphost" class="form-label">Hostname or IP address</label>
        <input type="text" id="coredump_tftphost" name="coredump_tftphost" class="form-control" value="<%= $coredump_tftphost %>">
      </p>
    </div>

    <div class="col">
      <h3>Upload to FTP server</h3>
      <p class="boolean">
        <span class="form-check form-switch">
          <input type="hidden" name="coredump_send2ftp" id="coredump_send2ftp-false" value="false">
          <input type="checkbox" id="coredump_send2ftp" name="coredump_send2ftp" value="true" class="form-check-input" role="switch"<% [ "true" = "$coredump_send2ftp" ] && echo " checked" %>>
          <label for="coredump_send2ftp" class="form-label form-check-label">Upload to FTP server</label>
        </span>
      </p>
      <p class="string">
        <label for="coredump_ftphost" class="form-label">Hostname or IP address</label>
        <input type="text" id="coredump_ftphost" name="coredump_ftphost" class="form-control" value="<%= $coredump_ftphost %>">
      </p>
      <p class="string">
        <label for="coredump_ftppath" class="form-label">Target directory</label>
        <input type="text" id="coredump_ftppath" name="coredump_ftppath" class="form-control" value="<%= $coredump_ftppath %>">
        <span class="hint text-secondary">relative to ftp root directory</span>
      </p>
      <p class="string">
        <label for="coredump_ftpuser" class="form-label">Username</label>
        <input type="text" id="coredump_ftpuser" name="coredump_ftpuser" class="form-control" value="<%= $coredump_ftpuser %>">
      </p>
      <p class="password">
        <label for="coredump_ftppass" class="form-label">Password</label>
        <span class="input-group">
          <input type="password" id="coredump_ftppass" name="coredump_ftppass" class="form-control"  value="<%= $coredump_ftppass %>">
          <label class="input-group-text"><input class="form-check-input me-1" type="checkbox" data-for="coredump_ftppass"> show</label>
        </span>
      </p>
    </div>
  </div>

  <h3>Log of last core dumping</h3>
  <% [ -f /root/coredump.log ] && ex "cat /root/coredump.log" %>

  <p class="mt-2"><input type="submit" class="btn btn-primary" value="Save changes"></p>
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
