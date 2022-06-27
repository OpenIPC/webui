#!/usr/bin/haserl
Date: <%= $(TZ=GMT0 date +"%a, %d %b %Y %T %Z") %>
Server: <%= $SERVER_SOFTWARE %>
Content-type: text/html; charset=UTF-8
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
<body id="page-<%= $pagename %>">
  <nav class="navbar navbar-dark navbar-expand-lg sticky-top">
    <div class="container">
      <a class="navbar-brand" href="/cgi-bin/status.cgi"><img alt="Image: OpenIPC logo" height="32" src="/a/logo.svg"></a>
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
              <li><a class="dropdown-item" href="/cgi-bin/status.cgi">Overview</a></li>
              <li><a class="dropdown-item" href="/cgi-bin/info-cron.cgi">Cron config</a></li>
              <li><a class="dropdown-item" href="/cgi-bin/info-majestic.cgi">Majestic config</a></li>
              <li><a class="dropdown-item" href="/cgi-bin/info-dmesg.cgi">Diagnostic messages</a></li>
              <li><a class="dropdown-item" href="/cgi-bin/info-httpd.cgi">HTTPd environment</a></li>
              <li><a class="dropdown-item" href="/cgi-bin/info-log.cgi">Log read</a></li>
              <li><a class="dropdown-item" href="/cgi-bin/info-overlay.cgi">Overlay partition</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownUpdates" role="button">Updates</a>
            <ul aria-labelledby="dropdownUpdates" class="dropdown-menu">
              <li><a  class="dropdown-item" href="/cgi-bin/firmware.cgi">Firmware</a></li>
              <li><a  class="dropdown-item" href="/cgi-bin/webui.cgi">Web Interface</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownSettings" role="button">Settings</a>
            <ul aria-labelledby="dropdownSettings" class="dropdown-menu">
              <li><a class="dropdown-item" href="/cgi-bin/majestic-settings.cgi">Majestic Settings</a></li>
              <li><a class="dropdown-item" href="/cgi-bin/network.cgi">Network Settings</a></li>
              <li><a class="dropdown-item" href="/cgi-bin/network-tz.cgi">System Timezone</a></li>
              <li><a class="dropdown-item" href="/cgi-bin/network-ntp.cgi">NTP Settings</a></li>
              <li><a class="dropdown-item" href="/cgi-bin/network-socks5.cgi">SOCKS5 Proxy</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownMajestic" role="button">Majestic</a>
            <ul aria-labelledby="dropdownMajestic" class="dropdown-menu">
              <li><a class="dropdown-item" href="/cgi-bin/majestic-config-actions.cgi">Majestic Maintenance</a></li>
              <li><a class="dropdown-item" href="/cgi-bin/majestic-debug.cgi">Majestic Debugging</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownTools" role="button">Tools</a>
            <ul aria-labelledby="dropdownTools" class="dropdown-menu">
              <li><a class="dropdown-item" href="/cgi-bin/tools.cgi">Ping & Traceroute</a></li>
              <li><a class="dropdown-item" href="/cgi-bin/console.cgi">Web Console</a></li>
              <li><a class="dropdown-item" href="/cgi-bin/ssh-keys.cgi">SSH Key</a></li>
              <li><a class="dropdown-item" href="/cgi-bin/sdcard.cgi">SD Card</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownServices" role="button">Services</a>
            <ul aria-labelledby="dropdownServices" class="dropdown-menu">
              <% load_plugins %>
            </ul>
          </li>
          <li class="nav-item"><a class="nav-link" href="/cgi-bin/preview.cgi">Preview</a></li>
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownHelp" role="button">Help</a>
            <ul aria-labelledby="dropdownHelp" class="dropdown-menu">
              <li><a class="dropdown-item" href="/cgi-bin/about.cgi">About OpenIPC</a></li>
              <li><a class="dropdown-item" href="/cgi-bin/endpoints.cgi">Endpoints</a></li>
              <li><a class="dropdown-item" href="https://openipc.org/wiki/">OpenIPC Wiki</a></li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <main>
    <div class="container">
      <p class="text-end x-small"><% signature %></p>

      <h2><%= $page_title %></h2>
      <% flash_read %>

<% if [ "true" = "$telegram_socks5_enabled" ] || [ "true" = "$yadisk_socks5_enabled" ]; then
  if [ -z "$socks5_server" ] || [ -z "$socks5_port" ]; then %>
<p class="alert alert-danger">You want to use SOCKS5 proxy but it is not configured!
  Please <a href="/cgi-bin/network-socks5.cgi">configure the proxy</a>.</p>
<% fi; fi %>
