#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_hardware_info
get_firmware_info
get_software_info

page_title="$tPageTitleFirmware"

# firmware data
fw_date=$(date -D "%a, %d %b %Y %T GMT" +"2.2.%m.%d" --date "$(curl -ILs https://github.com/OpenIPC/firmware/releases/download/latest/openipc.${soc}-br.tgz | grep Last-Modified | cut -d' ' -f2-)")

# NB! size in allocated blocks.
mj_filesize_fw=$(ls -s $mj_bin_file | xargs | cut -d' ' -f1)
if [ -f "/overlay/$mj_bin_file" ]; then
  mj_filesize_overlay=$(ls -s /overlay/$mj_bin_file | xargs | cut -d' ' -f1)
  mj_filesize_old=$mj_filesize_overlay
else
  mj_filesize_old=$mj_filesize_fw
fi

# re-download metafile if older than 1 hour
mj_meta_url="http://openipc.s3-eu-west-1.amazonaws.com/majestic.${soc_family}.${fw_variant}.master.tar.meta"
mj_meta_file=/tmp/mj_meta.txt
mj_meta_file_timestamp=$(date +%s --date "$(ls -lc --full-time $mj_meta_file | xargs | cut -d' ' -f6,7)")
mj_meta_file_expiration=$(( $(date +%s) + 3600 ))
if [ ! -f "$mj_meta_file" ] || [ "$mj_meta_file_timestamp" -gt "$mj_meta_file_expiration" ]; then
  curl -s $mj_meta_url -o $mj_meta_file
fi
# parse version, date and file size
if [ "$(wc -l $mj_meta_file | cut -d' ' -f1)" = "1" ]; then
  mj_filesize_new=$(sed -n 1p $mj_meta_file)
else
  mj_version_new=$(sed -n 1p $mj_meta_file)
  mj_filesize_new=$(sed -n 2p $mj_meta_file)
fi
# NB! size in bytes, but since blocks are 1024 bytes each, we are safe here for now.
mj_filesize_new=$(( ($mj_filesize_new + 1024) / 1024 )) # Rounding up by priming, since $(()) sucks at floats.

free_space=$(df | grep /overlay | xargs | cut -d' ' -f4)
free_space=$(df /overlay | tail -1 | xargs | awk '{print $5}')
available_space=$(( $free_space + $mj_filesize_overlay - 1 ))
%>
<%in _header.cgi %>
<%
alert_ "danger"
  h6 "$tMsgDestructiveActions"
  p "$tMsgKnowWhatYouDo"
_alert

row_ "row-cols-1 row-cols-md-2 row-cols-xl-3 g-3 mb-3"
  col_card_ "$tHeaderFirmware"
    dl_ "class=\"row small\""
      dt "$tInstalled" "class=\"col-4\""
      dd "$fw_version" "class=\"col-8 text-end\""
      dt "$tLastAvailable" "class=\"col-4\""
      dd "$fw_date" "class=\"col-8 text-end\" id=\"firmware-master-ver\""
    _dl

    fw_kernel="true"
    fw_rootfs="true"

    alert_ "light"
      h6 "$tInstallUpdate"
      form_ "/cgi-bin/firmware-update.cgi" "post"
        field_checkbox "fw_kernel"
        field_checkbox "fw_rootfs"
        field_checkbox "fw_reset"
        field_checkbox "fw_noreboot"
        field_checkbox "fw_enforce"
        button_submit "$tButtonInstallUpdate" "warning"
      _form
    _alert
%>
<%in parts/reset-firmware.cgi %>
<%
  _col_card

  col_card_ "$tHeaderWebui"
    dl_ "class=\"row small\""
      dt "$tInstalled" "class=\"col-4\""
      dd "$ui_version" "class=\"col-8 text-end\""
      dt "$tStable" "class=\"col-4\""
      dd "" "class=\"col-8 text-end\" id=\"microbe-web-master-ver\""
      dt "$tUnstable" "class=\"col-4\""
      dd "" "class=\"col-8 text-end\" id=\"microbe-web-dev-ver\""
    _dl

    alert_ "light"
      h6 "$tInstallUpdate"
      form_ "/cgi-bin/webui-update.cgi" "post"
        field_select "web_version"
        field_checkbox "web_enforce"
        button_submit "$tButtonInstallUpdate" "warning"
      _form
    _alert
  _col_card

  col_card_ "Majestic"
    dl_ "class=\"row small\""
      dt "$tInstalled" "class=\"col-4\""
      dd "$mj_version" "class=\"col-8 text-end\""
      dt "$tLastAvailable" "class=\"col-4\""
      dd "$mj_version_new" "class=\"col-8 text-end\""
    _dl

    alert_ "light"
      if [ -f "/overlay/root/${mj_mj_bin_file}" ]; then
        h6 "$tMjInOverlay ($mj_filesize_overlay KB)"
      else
        h6 "$tMjInBundle"
      fi

      if [ "$mj_filesize_new" -le "$available_space" ]; then
        form_ "/cgi-bin/majestic-github.cgi" "post"
          button "$tButtonInstallUpdate" "warning"
        _form
      else
        alert "$tMjNoSpace" "warning"
        # ${mj_filesize_new}K
      fi
    _alert


    if [ -z "$(diff /rom/etc/majestic.yaml /etc/majestic.yaml)" ]; then
      alert_ "light"
        h6 "$tMjConfigUnchanged"
        link_to "$tMjConfigEdit" "/cgi-bin/majestic-settings.cgi"
      _alert
    else
      alert_ "light"
        h6 "$tMjConfigChanged"
        link_to "$tMjConfigSeeChanges" "/cgi-bin/majestic-config-compare.cgi"
      _alert

      alert_ "danger"
        h6 "$tMjConfigReset"
        p "$tMjConfigResetInfo"
        button_link_to "$tMjConfigBackup" "/cgi-bin/majestic-config-backup.cgi" "primary"
        button_link_to "$tButtonMjReset" "/cgi-bin/majestic-config-reset.cgi" "danger" "title=\"$tMjConfigResetTitle\""
      _alert
    fi
  _col_card

  col_card_ "$tHeaderCamera"
    button_link_to "$tRebootCamera" "/cgi-bin/reboot.cgi" "warning"
  _col_card

  col_card_ "$tHeaderUploadKernel"
    form_ "/cgi-bin/firmware-upload-kernel.cgi" "post" "enctype=\"multipart/form-data\""
      field_file "kernel_file"
      button_submit "$tButtonUploadFile" "danger"
    _form
  _col_card

  col_card_ "$tHeaderUploadRootfs"
    form_ "/cgi-bin/firmware-upload-rootfs.cgi" "post" "enctype=\"multipart/form-data\""
      field_file "rootfs_file"
      button_submit "$tButtonUploadFile" "danger"
    _form
  _col_card
_row
%>

<script>
const GH_URL="https://github.com/OpenIPC/";
const GH_API="https://api.github.com/repos/OpenIPC/";

function checkUpdates() {
  queryBranch('microbe-web', 'master');
  queryBranch('microbe-web', 'dev');
}

function queryBranch(repo, branch) {
  var oReq = new XMLHttpRequest();
  oReq.addEventListener("load", function(){
    const d = JSON.parse(this.response);
    const sha_short = d.commit.sha.slice(0,7);
    const date = d.commit.commit.author.date.slice(0,10);
    const link = document.createElement('a');
    link.href = GH_URL + repo + '/commits/' + branch;
    link.target = '_blank';
    link.textContent = branch + '+' + sha_short + ', ' + date;
    const el = $('#' + repo + '-' + branch + '-ver').appendChild(link);
  });
  oReq.open("GET", GH_API + repo + '/branches/' + branch);
  oReq.send();
}

window.addEventListener('load', checkUpdates);
</script>
<%in _footer.cgi %>
