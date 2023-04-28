#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Firmware"
if [ -n "$network_gateway" ]; then
  case "$soc" in
   # Ingenic firmware does not correspond to SoC model
   t10*) url="https://github.com/OpenIPC/firmware/releases/download/latest/openipc.t10-lite-nor.tgz" ;;
   t20*) url="https://github.com/OpenIPC/firmware/releases/download/latest/openipc.t20-lite-nor.tgz" ;;
   t21*) url="https://github.com/OpenIPC/firmware/releases/download/latest/openipc.t21-lite-nor.tgz" ;;
   t31*) url="https://github.com/OpenIPC/firmware/releases/download/latest/openipc.t31-line-nor.tgz" ;;
      *) url="https://github.com/OpenIPC/firmware/releases/download/latest/openipc.${soc}-${flash_type}-${fw_variant}.tgz" ;;
  esac
  fw_date=$(date -D "%a, %d %b %Y %T GMT" +"2.3.%m.%d" --date "$(curl -ILs "$url" | grep Last-Modified | cut -d' ' -f2-)")
else
  fw_date="<span class=\"text-danger\">- no access to GitHub -</span>"
fi
fw_kernel="true"
fw_rootfs="true"
%>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <h3>Version</h3>
      <dl class="list small">
      <dt>Installed</dt>
      <dd><%= $fw_version %></dd>
      <dt>On GitHub</dt>
      <dd id="firmware-master-ver"><%= $fw_date %></dd>
    </dl>
  </div>
  <div class="col">
    <h3>Upgrade</h3>
    <% if [ -n "$network_gateway" ]; then %>
      <form action="firmware-update.cgi" method="post">
        <% field_checkbox "fw_kernel" "Upgrade kernel." %>
        <% field_checkbox "fw_rootfs" "Upgrade rootfs." %>
        <% field_checkbox "fw_reset" "Reset firmware." %>
        <% field_checkbox "fw_noreboot" "Do not reboot after upgrade." %>
        <% field_checkbox "fw_enforce" "Install even if matches the existing version." %>
        <% button_submit "Install update from GitHub" "warning" %>
      </form>
    <% else %>
      <p class="alert alert-danger">Upgrading requires access to GitHub.</p>
    <% fi %>
  </div>
  <div class="col">
    <h3>Upload Kernel & RootFS</h3>
    <form action="firmware-upload-parts.cgi" method="post" enctype="multipart/form-data">
      <% field_file "parts_file" "Binary file" %>
      <% field_select "parts_type" "Type of the binary file" "kernel,rootfs" %>
      <p class="text-danger small">Destructive! Make sure you know what you are doing.</p>
      <% button_submit "Upload file" "danger" %>
    </form>
  </div>
</div>

<%in p/footer.cgi %>
