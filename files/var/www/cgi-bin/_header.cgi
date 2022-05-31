#!/usr/bin/haserl
Content-Type: text/html; charset=UTF-8

<%
get_hardware_info
get_firmware_info
get_system_info
%>
<!DOCTYPE html>
<html lang="<%= $locale %>">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title><% html_title "$page_title" %></title>
<link rel="shortcut icon" href="/img/favicon.png">
<link rel="stylesheet" href="/css/bootstrap.min.css">
<link rel="stylesheet" href="/css/bootstrap.override.css">
<% if [ $HTTP_MODE = "development" ]; then %><link rel="stylesheet" href="/css/debug.css"><% fi %>
<script src="/js/bootstrap.bundle.min.js"></script>
<script src="/js/main.js"></script>
</head>

<body id="top">
<nav class="navbar navbar-expand-lg navbar-dark sticky-top">
  <div class="container">
    <a class="navbar-brand" href="/cgi-bin/status.cgi"><img src="/img/logo.svg" width="116" height="32" alt="">
      <div id="beta"><span><span><span><span>beta</span></span></span></span></div></a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
      aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" id="dropdownInformation" href="#"
            role="button" data-bs-toggle="dropdown" aria-expanded="false"><%= $tMenuInformation %></a>
          <ul class="dropdown-menu" aria-labelledby="dropdownInformation">
            <li><a class="dropdown-item" href="/cgi-bin/status.cgi"><%= $tMenuOverview %></a></li>
            <li><a class="dropdown-item" href="/cgi-bin/info-cron.cgi"><%= $tMenuCron %></a></li>
            <li><a class="dropdown-item" href="/cgi-bin/info-dmesg.cgi"><%= $tMenuDmesg %></a></li>
            <li><a class="dropdown-item" href="/cgi-bin/info-httpd-config.cgi"><%= $tMenuHttpd %></a></li>
            <li><a class="dropdown-item" href="/cgi-bin/info-httpd.cgi"><%= $tMenuHttpdEnv %></a></li>
            <li><a class="dropdown-item" href="/cgi-bin/info-log.cgi"><%= $tMenuLog %></a></li>
            <li><a class="dropdown-item" href="/cgi-bin/info-overlay.cgi"><%= $tMenuOverlay %></a></li>
          </ul>
        </li>
        <li class="nav-item"><a class="nav-link" href="/cgi-bin/firmware.cgi"><%= $tMenuFirmware %></a></li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" id="dropdownNetwork" href="#"
            role="button" data-bs-toggle="dropdown" aria-expanded="false"><%= $tMenuSettings %></a>
          <ul class="dropdown-menu" aria-labelledby="dropdownNetwork">
            <li><a class="dropdown-item" href="/cgi-bin/network.cgi"><%= $tMenuNetwork %></a></li>
            <li><a class="dropdown-item" href="/cgi-bin/network-ntp.cgi"><%= $tMenuNtp %></a></li>
            <li><a class="dropdown-item" href="/cgi-bin/webui-settings.cgi"><%= $tMenuWebUi %></a></li>
          </ul>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" id="dropdownMajestic" href="#"
            role="button" data-bs-toggle="dropdown" aria-expanded="false">Majestic</a>
          <ul class="dropdown-menu" aria-labelledby="dropdownMajestic">
            <li><a class="dropdown-item" href="/cgi-bin/majestic-settings.cgi"><%= $tMenuMjSettings %> (new UI)</a></li>
            <li><a class="dropdown-item" href="/cgi-bin/majestic-settings-general.cgi"><%= $tMenuMjSettings %></a></li>
            <li><a class="dropdown-item" href="/cgi-bin/majestic-settings-services.cgi"><%= $tMenuMjServices %></a></li>
            <li><a class="dropdown-item" href="/cgi-bin/majestic-config-actions.cgi"><%= $tMenuMjMaintenance %></a></li>
            <li><a class="dropdown-item" href="/cgi-bin/majestic-debug.cgi"><%= $tMenuMjDebug %></a></li>
            <li><a class="dropdown-item" href="/cgi-bin/preview-help.cgi"><%= $tMenuMjInformation %></a></li>
          </ul>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" id="dropdownTools" href="#"
            role="button" data-bs-toggle="dropdown" aria-expanded="false"><%= $tMenuTools %></a>
          <ul class="dropdown-menu" aria-labelledby="dropdownTools">
            <li><a class="dropdown-item" href="/cgi-bin/tools.cgi"><%= $tMenuPingTrace %></a></li>
            <li><a class="dropdown-item" href="/cgi-bin/console.cgi"><%= $tMenuWebConsole %></a></li>
            <li><a class="dropdown-item" href="/cgi-bin/ssh-keys.cgi"><%= $tMenuSshKeys %></a></li>
            <li><a class="dropdown-item" href="/cgi-bin/sdcard.cgi"><%= $tMenuSdCard %></a></li>
          </ul>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" id="dropdownServices" href="#"
            role="button" data-bs-toggle="dropdown" aria-expanded="false"><%= $tMenuServices %></a>
          <ul class="dropdown-menu" aria-labelledby="dropdownServices">
            <li><a class="dropdown-item" href="/cgi-bin/plugin-bigbro.cgi"><%= $tMenuPluginBigbro %></a></li>
            <li><a class="dropdown-item" href="/cgi-bin/plugin-ipeye.cgi"><%= $tMenuPluginIpeye %></a></li>
            <li><a class="dropdown-item" href="/cgi-bin/plugin-telegram.cgi"><%= $tMenuPluginTelegram %></a></li>
            <li><a class="dropdown-item" href="/cgi-bin/plugin-vtun.cgi"><%= $tMenuPluginVtun %></a></li>
          </ul>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" id="dropdownPreview" href="#"
            role="button" data-bs-toggle="dropdown" aria-expanded="false"><%= $tMenuPreview %></a>
          <ul class="dropdown-menu" aria-labelledby="dropdownPreview">
            <li><a class="dropdown-item" href="/cgi-bin/preview.cgi">JPEG</a></li>
            <li><a class="dropdown-item" href="/cgi-bin/preview-mjpeg.cgi">MJPEG</a></li>
            <li><a class="dropdown-item" href="/cgi-bin/preview-video.cgi">Video</a></li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</nav>
<div class="bg-light text-end x-small p-2">
  <div class="container">
    <%= "$soc ($soc_family family), $sensor, $flash_size MB Flash. ${fw_version}-${fw_variant}. $hostname, $wan_mac" %>
  </div>
</div>
<main>
  <div class="container p-3">
    <h2><%= $page_title %></h2>
    <% flash_read %>
