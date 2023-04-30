#!/usr/bin/haserl
Content-type: text/html; charset=UTF-8
Date: <%= $(TZ=GMT0 date +'%a, %d %b %Y %T %Z') %>
Server: <%= $SERVER_SOFTWARE %>
Cache-Control: no-store
Pragma: no-cache

<!DOCTYPE html>
<html lang="<%= ${locale:=en} %>" data-bs-theme="<%= ${webui_theme:=light} %>">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title><% html_title %></title>
<link rel="stylesheet" href="/a/bootstrap.min.css">
<link rel="stylesheet" href="/a/bootstrap.override.css">
<script src="/a/bootstrap.bundle.min.js"></script>
<script src="/a/main.js"></script>
</head>

<body id="page-<%= $pagename %>" class="<%= $fw_variant %> <%= ${webui_level:-user} %><% [ "$debug" -ge "1" ] && echo -n " debug" %>">
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container">
      <a class="navbar-brand" href="status.cgi"><img alt="Image: OpenIPC logo" height="32" src="/a/logo.svg"><span class="x-small ms-1"><%= $fw_variant %></span></a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownInformation" role="button">Information</a>
            <ul aria-labelledby="dropdownInformation" class="dropdown-menu">
              <li><a class="dropdown-item" href="status.cgi">Overview</a></li>
              <li><a class="dropdown-item" href="info-cron.cgi">Cron config</a></li>
              <li><a class="dropdown-item" href="info-dmesg.cgi">Diagnostic messages</a></li>
              <li><a class="dropdown-item" href="info-httpd.cgi">HTTPd environment</a></li>
              <li><a class="dropdown-item" href="info-modules.cgi">Modules</a></li>
              <li><a class="dropdown-item" href="info-proc-umap.cgi">Information from /proc/umap</a></li>
              <li><a class="dropdown-item" href="info-ipctool.cgi">IPC Tool</a></li>
              <li><a class="dropdown-item" href="info-netstat.cgi">Network stats</a></li>
              <li><a class="dropdown-item" href="info-log.cgi">Log read</a></li>
              <li><a class="dropdown-item" href="info-overlay.cgi">Overlay partition</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownUpdates" role="button">Updates</a>
            <ul aria-labelledby="dropdownUpdates" class="dropdown-menu">
              <li><a class="dropdown-item" href="firmware.cgi">Firmware</a></li>
              <li><a class="dropdown-item" href="webui.cgi">Web Interface</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownSettings" role="button">Settings</a>
            <ul aria-labelledby="dropdownSettings" class="dropdown-menu">
              <li><a class="dropdown-item" href="network.cgi">Network</a></li>
              <li><a class="dropdown-item" href="time-config.cgi">Time</a></li>
              <li><a class="dropdown-item" href="network-socks5.cgi">SOCKS5 Proxy</a></li>
              <li><a class="dropdown-item" href="webui-settings.cgi">Web Interface</a></li>
              <li><a class="dropdown-item" href="admin.cgi">Admin Profile</a></li>
              <li><a class="dropdown-item" href="debugging.cgi">Debugging</a></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="reset.cgi">Reset...</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownMajestic" role="button">Majestic</a>
            <ul aria-labelledby="dropdownMajestic" class="dropdown-menu">
<%
mj=$(echo "$mj" | sed "s/ /_/g")
for _line in $mj; do
  _parameter=${_line%%|*};
  _param_name=${_parameter#.};
  _param_domain=${_param_name%.*}
  if [ "$_parameter_domain_old" != "$_param_domain" ]; then
    # hide certain domains if not supported
    [ -n "$(eval echo "\$mj_hide_${_param_domain}" | sed -n "/\b${soc_family}\b/p")" ] && continue
    [ -n "$(eval echo "\$mj_show_${_param_domain}_vendor")" ] && [ -z "$(eval echo "\$mj_show_${_param_domain}_vendor" | sed -n "/\b${soc_vendor}\b/p")" ] && continue
    _parameter_domain_old="$_param_domain"
    _css="class=\"dropdown-item\""; [ "$_param_domain" = "$only" ] && _css="class=\"dropdown-item active\" aria-current=\"true\""
    echo "<li><a ${_css} href=\"majestic-settings.cgi?tab=${_param_domain}\">$(eval echo \$tT_mj_${_param_domain})</a></li>"
  fi
done
unset _css; unset _param_domain; unset _line; unset _param_name; unset _parameter_domain_old; unset _parameter;
%>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="info-majestic.cgi">Majestic YAML</a></li>
              <li><a class="dropdown-item" href="majestic-endpoints.cgi">Majestic Endpoints</a></li>
              <li><a class="dropdown-item" href="majestic-config-actions.cgi">Majestic Maintenance</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownTools" role="button">Tools</a>
            <ul aria-labelledby="dropdownTools" class="dropdown-menu">
              <li><a class="dropdown-item" href="tools.cgi">Ping & Traceroute</a></li>
              <li><a class="dropdown-item" href="console.cgi">Web Console</a></li>
              <li><a class="dropdown-item" href="file-manager.cgi">File Manager</a></li>
              <li><a class="dropdown-item" href="ssh-keys.cgi">SSH Key</a></li>
              <li><a class="dropdown-item" href="sdcard.cgi">SD Card</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownServices" role="button">Services</a>
            <ul aria-labelledby="dropdownServices" class="dropdown-menu">
              <% load_plugins %>
            </ul>
          </li>
          <li class="nav-item"><a class="nav-link" href="preview.cgi">Preview</a></li>
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownHelp" role="button">Help</a>
            <ul aria-labelledby="dropdownHelp" class="dropdown-menu dropdown-menu-lg-end">
              <li><a class="dropdown-item" href="https://openipc.org/">About OpenIPC</a></li>
              <li><a class="dropdown-item" href="https://openipc.org/wiki/">OpenIPC Wiki</a></li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <main class="pb-4">
    <div class="container" style="min-height: 90vh">
      <div class="row mt-1 x-small">
        <div class="col-lg-2">
          <div id="pb-memory" class="progress my-1" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"><div class="progress-bar"></div></div>
          <div id="pb-overlay" class="progress my-1" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"><div class="progress-bar"></div></div>
        </div>
        <div class="col-md-7 mb-2">
          <%= $(signature) %>
        </div>
        <div class="col-md-4 col-lg-3 mb-2 text-end">
          <div id="time-now"></div>
          <div id="soc-temp"></div>
        </div>
      </div>
<% if [ -z "$network_gateway" ]; then %>
<div class="alert alert-warning">
<p class="mb-0">No Internet connection. Please <a href="network.cgi">check your network settings</a>.</p>
</div>
<% fi %>

<% if [ "true" = "$openwall_socks5_enabled" ] || [ "true" = "$telegram_socks5_enabled" ] || [ "true" = "$yadisk_socks5_enabled" ]; then
  if [ -z "$socks5_host" ] || [ -z "$socks5_port" ]; then %>
<div class="alert alert-danger">
<p class="mb-0">You want to use SOCKS5 proxy but it is not configured! Please <a href="network-socks5.cgi">configure the proxy</a>.</p>
</div>
<% fi; fi %>

<% if [ "true" = "$speaker_enabled" ] && [ "true" != "$(yaml-cli -g .audio.enabled)" ]; then %>
<div class="alert alert-danger">
<p class="mb-0">You need to enable audio in <a href="majestic-settings.cgi?tab=audio">Majestic settings.</a></p>
</div>
<% fi %>

<% if [ "$(cat /etc/TZ)" != "$TZ" ]; then %>
<div class="alert alert-danger">
<p>$TZ variable in system environment needs updating!</p>
<span class="d-flex gap-3">
<a class="btn btn-danger" href="reboot.cgi">Reboot camera</a>
<a class="btn btn-primary" href="timezone.cgi">See timezone settings</a>
</span>
</div>
<% fi %>

<% if [ -f /tmp/network-restart.txt ]; then %>
<div class="alert alert-danger">
<p>Network settings have been updated. Restart to apply changes.</p>
<span class="d-flex gap-3">
<a class="btn btn-danger" href="reboot.cgi">Reboot camera</a>
<a class="btn btn-primary" href="network.cgi">See network settings</a>
</span>
</div>
<% fi %>

<% if [ -f /tmp/coredump-restart.txt ]; then %>
<div class="alert alert-danger">
<p>Majestic debugging settings have been updated. Restart to apply changes.</p>
<span class="d-flex gap-3">
<a class="btn btn-danger" href="reboot.cgi">Reboot camera</a>
<a class="btn btn-primary" href="debugging.cgi">See debugging settings</a>
</span>
</div>
<% fi %>

<% if [ -f /tmp/motionguard-restart.txt ]; then %>
<div class="alert alert-danger">
<p>Changes to motion guard configuration detected. Please restart camera to apply the changes.</p>
<span class="d-flex gap-3">
<a class="btn btn-danger" href="reboot.cgi">Reboot camera</a>
<a class="btn btn-primary" href="plugin-motion.cgi">See motion guard settings</a>
</span>
</div>
<% fi %>

<h2><%= $page_title %></h2>
<% flash_read %>
