#!/usr/bin/haserl
Content-type: text/html; charset=UTF-8
Date: <%= $(TZ=GMT0 date +'%a, %d %b %Y %T %Z') %>
Server: <%= $SERVER_SOFTWARE %>
Cache-Control: no-store
Pragma: no-cache

<!DOCTYPE html>
<html lang="<%= $locale %>">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title><% html_title "$page_title" %></title>
<link rel="stylesheet" href="/a/bootstrap.css">
<link rel="stylesheet" href="/a/bootstrap.override.css">
<script src="/a/bootstrap.js"></script>
<script src="/a/main.js"></script>
</head>

<body id="page-<%= $pagename %>" class="<%= $fw_variant %><% [ "$debug" -ge "1" ] && echo -n " debug" %>">
  <nav class="navbar navbar-dark navbar-expand-lg sticky-top">
    <div class="container">
      <a class="navbar-brand" href="status.cgi"><img alt="Image: OpenIPC logo" height="32" src="/a/logo.svg">
       <span class="x-small"><%= $fw_variant %></span></a>
      <% if [ -n "$soc_temp" ]; then %>
        <span id="soc-temp" class="text-primary bg-white rounded small" title="<%= $tSoCTemp %>"><%= $soc_temp %>°C</span>
      <% fi %>
      <button aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation" class="navbar-toggler" data-bs-target="#navbarNav" data-bs-toggle="collapse" type="button">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownInformation" role="button">Information</a>
            <ul aria-labelledby="dropdownInformation" class="dropdown-menu">
              <li><a class="dropdown-item" href="status.cgi">Overview</a></li>
              <li><a class="dropdown-item" href="info-cron.cgi">Cron config</a></li>
              <li><a class="dropdown-item" href="info-majestic.cgi">Majestic config</a></li>
              <li><a class="dropdown-item" href="info-dmesg.cgi">Diagnostic messages</a></li>
              <li><a class="dropdown-item" href="info-httpd.cgi">HTTPd environment</a></li>
              <li><a class="dropdown-item" href="info-modules.cgi">Modules</a></li>
              <li><a class="dropdown-item" href="info-log.cgi">Log read</a></li>
              <li><a class="dropdown-item" href="info-overlay.cgi">Overlay partition</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownUpdates" role="button">Updates</a>
            <ul aria-labelledby="dropdownUpdates" class="dropdown-menu">
              <li><a class="dropdown-item" href="firmware.cgi">Firmware</a></li>
              <li><a class="dropdown-item" href="majestic.cgi">Majestic</a></li>
              <li><a class="dropdown-item" href="webui.cgi">Web Interface</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownSettings" role="button">Settings</a>
            <ul aria-labelledby="dropdownSettings" class="dropdown-menu">
              <li><a class="dropdown-item" href="network.cgi">Network</a></li>
              <li><a class="dropdown-item" href="timezone.cgi">Timezone</a></li>
              <li><a class="dropdown-item" href="network-ntp.cgi">Time Synchronization</a></li>
              <li><a class="dropdown-item" href="network-socks5.cgi">SOCKS5 Proxy</a></li>
              <li><a class="dropdown-item" href="majestic-settings.cgi">Majestic Streamer</a></li>
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
              <li><a class="dropdown-item" href="majestic-config-actions.cgi">Majestic Maintenance</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownTools" role="button">Tools</a>
            <ul aria-labelledby="dropdownTools" class="dropdown-menu">
              <li><a class="dropdown-item" href="tools.cgi">Ping & Traceroute</a></li>
              <li><a class="dropdown-item" href="console.cgi">Web Console</a></li>
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
            <ul aria-labelledby="dropdownHelp" class="dropdown-menu">
              <li><a class="dropdown-item" href="https://openipc.org/">About OpenIPC</a></li>
              <li><a class="dropdown-item" href="endpoints.cgi">Endpoints</a></li>
              <li><a class="dropdown-item" href="https://openipc.org/wiki/">OpenIPC Wiki</a></li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <main>
    <div class="container">
      <p class="text-end x-small"><%= $(signature) %></p>

<% if [ -z "$network_gateway" ]; then %>
<div class="alert alert-warning">
<p class="mb-0">No Internet connection. Please <a href="network.cgi">check your network settings</a>.</p>
</div>
<% fi %>

<% if [ "true" = "$telegram_socks5_enabled" ] || [ "true" = "$yadisk_socks5_enabled" ]; then
  if [ -z "$socks5_host" ] || [ -z "$socks5_port" ]; then %>
<div class="alert alert-danger">
<p class="mb-0">You want to use SOCKS5 proxy but it is not configured! Please <a href="network-socks5.cgi">configure the proxy</a>.</p>
</div>
<% fi; fi %>

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
