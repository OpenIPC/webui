#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_hardware_info
get_firmware_info
get_software_info

fw_date=$(curl -ILs https://github.com/OpenIPC/firmware/releases/download/latest/openipc.hi3518ev100-br.tgz | grep Last-Modified | cut -d" " -f2-)
fw_date=$(date -d "$fw_date" -D "%a, %d %b %Y %T GMT" +"2.2.%m.%d")

page_title="$tPageTitleFirmware"
mj_meta_url="http://openipc.s3-eu-west-1.amazonaws.com/majestic.${soc_family}.${fw_variant}.master.tar.meta"
mj_config_diff=$(diff /rom/etc/majestic.yaml /etc/majestic.yaml)
[ -f /overlay/root/${mj_bin_file} ] && mj_filesize_old=$(ls -s ${mj_bin_file} | xargs | cut -d" " -f1) || mj_filesize_old=0
mj_filesize_new=$(curl -s ${mj_meta_url})
mj_filesize_new=$(echo $mj_filesize_new / 1024 | bc)
free_space=$(df | grep /overlay | xargs | cut -d" " -f4)
available_space=$(( $free_space + $mj_filesize_old - 1 ))
%>
<%in _header.cgi %>
<%
alert_ "danger"
  h6 "$tMsgDestructiveActions"
  p "$tMsgKnowWhatYouDo"
_alert

row_ "row-cols-1 row-cols-md-2 row-cols-xl-3 g-4 mb-4"
  col_card_ "$tHeaderFirmware"
    dl_ "class=\"row\""
      dt "$tInstalled" "class=\"col-4\""
      dd "$fw_version" "class=\"col-8 text-end\""
      dt "$tLatest" "class=\"col-4\""
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
    dl_ "class=\"row\""
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
    dl_ "class=\"row\""
      dt "$tInstalled" "class=\"col-4\""
      dd "$mj_version" "class=\"col-8 text-end\""
      dt "$tLatest" "class=\"col-4\""
      dd "" "class=\"col-8 text-end\" id=\"mj-ver-master\""
    _dl

    alert_ "light"
      if [ -f /overlay/root/usr/bin/majestic ]; then
        h6 "$tMjInOverlay ($mj_filesize_old KB)"
      else
        h6 "$tMjInBundle"
      fi
    _alert

    if [ "$mj_filesize_new" -le "$available_space" ]; then
      form_ "/cgi-bin/majestic-github.cgi" "post"
        button "$tButtonInstallUpdate" "warning"
      _form
    else
      alert "$tMjNoSpace" "warning"
    fi

    if [ -z "$mj_config_diff" ]; then
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

  col_card_ $tHeaderUploadRootfs
    form_ "/cgi-bin/firmware-upload-rootfs.cgi" "post" "enctype=\"multipart/form-data\""
      field_file "rootfs_file"
      button_submit "$tButtonUploadFile" "danger"
    _form
  _col_card
_row
%>

<script>
function checkUpdates() {
  //queryRelease();
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
    link.href = 'https://github.com/OpenIPC/' + repo + '/commits/' + branch;
    link.target = '_blank';
    link.textContent = branch + '+' + sha_short + ', ' + date;
    const el = $('#' + repo + '-' + branch + '-ver').appendChild(link);
  });
  oReq.open("GET", 'https://api.github.com/repos/OpenIPC/' + repo + '/branches/' + branch);
  oReq.send();
}
function queryRelease() {
  var oReq = new XMLHttpRequest();
  oReq.addEventListener("load", function(){
    const d = JSON.parse(this.response);
    const asset = d[0].assets.find(a => a['name'] === 'openipc.<%= $soc %>-br.tgz');
    const date = asset.created_at.slice(0,10);
    const sha_short = asset.target_commitish.slice(0,7);
    const link = document.createElement('a');
    link.href = 'https://github.com/OpenIPC/firmware/commits/master';
    link.target = '_blank';
    link.textContent = 'master+' + sha_short + ', ' + date;
    const el = $('#firmware-master-ver').appendChild(link);
  });
  oReq.open("GET", 'https://api.github.com/repos/OpenIPC/firmware/releases');
  oReq.send();
}
window.addEventListener('load', checkUpdates);
</script>
<%in _footer.cgi %>
