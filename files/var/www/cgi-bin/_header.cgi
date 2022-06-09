#!/usr/bin/haserl
Content-Type: text/html; charset=UTF-8
Cache-Control: no-store
Pragma: no-cache
Date: $(TZ=GMT date +"%a, %d %b %Y %T %Z")

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
    <a class="navbar-brand" href="/cgi-bin/status.cgi"><img src="/img/logo.svg" width="116" height="32" alt=""><div id="beta"><span><span><span><span>beta</span></span></span></span></div></a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" id="dropdownInformation" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false"><%= $tMenuInformation %></a>
          <ul class="dropdown-menu" aria-labelledby="dropdownInformation">
<%
dropdown_to "$tMenuOverview" "/cgi-bin/status.cgi"
dropdown_to "$tMenuCron" "/cgi-bin/info-cron.cgi"
dropdown_to "$tMenuDmesg" "/cgi-bin/info-dmesg.cgi"
dropdown_to "$tMenuHttpd" "/cgi-bin/info-httpd-config.cgi"
dropdown_to "$tMenuHttpdEnv" "/cgi-bin/info-httpd.cgi"
dropdown_to "$tMenuLog" "/cgi-bin/info-log.cgi"
dropdown_to "$tMenuOverlay" "/cgi-bin/info-overlay.cgi"
%>
          </ul>
        </li>
        <li class="nav-item"><a class="nav-link" href="/cgi-bin/firmware.cgi"><%= $tMenuFirmware %></a></li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" id="dropdownNetwork" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false"><%= $tMenuSettings %></a>
          <ul class="dropdown-menu" aria-labelledby="dropdownNetwork">
<%
dropdown_to "$tMenuNetwork" "/cgi-bin/network.cgi"
dropdown_to "$tMenuNtp" "/cgi-bin/network-ntp.cgi"
dropdown_to "$tMenuWebUi" "/cgi-bin/webui-settings.cgi"
%>
          </ul>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" id="dropdownMajestic" href="#"
            role="button" data-bs-toggle="dropdown" aria-expanded="false">Majestic</a>
          <ul class="dropdown-menu" aria-labelledby="dropdownMajestic">
<%
dropdown_to "$tMenuMjSettings" "/cgi-bin/majestic-settings.cgi"
dropdown_to "$tMenuMjMaintenance" "/cgi-bin/majestic-config-actions.cgi"
dropdown_to "$tMenuMjDebug" "/cgi-bin/majestic-debug.cgi"
dropdown_to "$tMenuMjInformation" "/cgi-bin/preview-help.cgi"
%>
          </ul>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" id="dropdownTools" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false"><%= $tMenuTools %></a>
          <ul class="dropdown-menu" aria-labelledby="dropdownTools">
<%
dropdown_to "$tMenuPingTrace" "/cgi-bin/tools.cgi"
dropdown_to "$tMenuWebConsole" "/cgi-bin/console.cgi"
dropdown_to "$tMenuSshKeys" "/cgi-bin/ssh-keys.cgi"
dropdown_to "$tMenuSdCard" "/cgi-bin/sdcard.cgi"
%>
          </ul>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" id="dropdownServices" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false"><%= $tMenuServices %></a>
          <ul class="dropdown-menu" aria-labelledby="dropdownServices">
<%
dropdown_to "$tMenuPluginBigbro" "/cgi-bin/plugin-bigbro.cgi"
dropdown_to "$tMenuPluginIpeye" "/cgi-bin/plugin-ipeye.cgi"
dropdown_to "$tMenuPluginTelegram" "/cgi-bin/plugin-telegram.cgi"
dropdown_to "$tMenuPluginVtun" "/cgi-bin/plugin-vtun.cgi"
%>
          </ul>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" id="dropdownPreview" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false"><%= $tMenuPreview %></a>
          <ul class="dropdown-menu" aria-labelledby="dropdownPreview">
<%
dropdown_to "JPEG" "/cgi-bin/preview.cgi"
dropdown_to "MJPEG" "/cgi-bin/preview-mjpeg.cgi"
dropdown_to "Video" "/cgi-bin/preview-video.cgi"
%>
          </ul>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" id="dropdownHelp" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false"><%= $tMenuHelp %></a>
          <ul class="dropdown-menu" aria-labelledby="dropdownHelp">
<%
dropdown_to "$tMenuWiki" "https://openipc.org/wiki/"
dropdown_to "$tMenuTelegram" "/cgi-bin/help-telegram.cgi"
dropdown_to "$tMenuAbout" "/cgi-bin/help-about.cgi"
%>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</nav>
<div class="bg-light text-end x-small p-2">
<div class="container"><%= "$soc ($soc_family family), $sensor, $flash_size MB Flash. ${fw_version}-${fw_variant}. $hostname, $wan_mac" %></div>
</div>

<main>
<%
div_ "class=\"container p-3\""

h2 "$page_title"

flash_read
%>
