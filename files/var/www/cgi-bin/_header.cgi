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
<%
link_css "/css/bootstrap.min.css"
link_css "/css/bootstrap.override.css"
[ "$HTTP_MODE" = "development" ] && link_css "/css/debug.css"
link_js "/js/bootstrap.bundle.min.js"
link_js "/js/main.js"
%>
</head>
<body id="top">
<%
nav_ "class=\"navbar navbar-expand-lg navbar-dark sticky-top\""
  container_
    link_to "$(image "/img/logo.svg" "height=\"32\"")" "/cgi-bin/status.cgi" "class=\"navbar-brand\""
    navbar_toggler "navbarNav"
    div_ "class=\"collapse navbar-collapse justify-content-end\" id=\"navbarNav\""
      ul_ "class=\"navbar-nav\""
        nav_dropdown_ "Information"
          nav_dropdown_to "$tMenuOverview" "/cgi-bin/status.cgi"
          nav_dropdown_to "$tMenuCron" "/cgi-bin/info-cron.cgi"
          nav_dropdown_to "$tMenuDmesg" "/cgi-bin/info-dmesg.cgi"
          nav_dropdown_to "$tMenuHttpd" "/cgi-bin/info-httpd-config.cgi"
          nav_dropdown_to "$tMenuHttpdEnv" "/cgi-bin/info-httpd.cgi"
          nav_dropdown_to "$tMenuLog" "/cgi-bin/info-log.cgi"
          nav_dropdown_to "$tMenuOverlay" "/cgi-bin/info-overlay.cgi"
        _nav_dropdown
        nav_item_link "$tMenuFirmware" "/cgi-bin/firmware.cgi"
        nav_dropdown_ "Settings"
          nav_dropdown_to "$tMenuNetwork" "/cgi-bin/network.cgi"
          nav_dropdown_to "$tMenuNtp" "/cgi-bin/network-ntp.cgi"
          nav_dropdown_to "$tMenuWebUi" "/cgi-bin/webui-settings.cgi"
        _nav_dropdown
        nav_dropdown_ "Majestic"
          nav_dropdown_to "$tMenuMjSettings" "/cgi-bin/majestic-settings.cgi"
          nav_dropdown_to "$tMenuMjMaintenance" "/cgi-bin/majestic-config-actions.cgi"
          nav_dropdown_to "$tMenuMjDebug" "/cgi-bin/majestic-debug.cgi"
          nav_dropdown_to "$tMenuMjInformation" "/cgi-bin/preview-help.cgi"
        _nav_dropdown
        nav_dropdown_ "Tools"
          nav_dropdown_to "$tMenuPingTrace" "/cgi-bin/tools.cgi"
          nav_dropdown_to "$tMenuWebConsole" "/cgi-bin/console.cgi"
          nav_dropdown_to "$tMenuSshKeys" "/cgi-bin/ssh-keys.cgi"
          nav_dropdown_to "$tMenuSdCard" "/cgi-bin/sdcard.cgi"
        _nav_dropdown
        nav_dropdown_ "Services"
          nav_dropdown_to "$tMenuPluginBigbro" "/cgi-bin/plugin-bigbro.cgi"
          nav_dropdown_to "$tMenuPluginIpeye" "/cgi-bin/plugin-ipeye.cgi"
          nav_dropdown_to "$tMenuPluginTelegram" "/cgi-bin/plugin-telegram.cgi"
          nav_dropdown_to "$tMenuPluginVtun" "/cgi-bin/plugin-vtun.cgi"
        _nav_dropdown
        nav_dropdown_ "Preview"
          nav_dropdown_to "JPEG" "/cgi-bin/preview.cgi"
          nav_dropdown_to "MJPEG" "/cgi-bin/preview-mjpeg.cgi"
          nav_dropdown_to "Video" "/cgi-bin/preview-video.cgi"
        _nav_dropdown
        nav_dropdown_ "Help"
          nav_dropdown_to "$tMenuWiki" "https://openipc.org/wiki/"
          nav_dropdown_to "$tMenuTelegram" "/cgi-bin/help-telegram.cgi"
          nav_dropdown_to "$tMenuAbout" "/cgi-bin/help-about.cgi"
        _nav_dropdown
      _ul
    _div
  _container
_nav

div_ "class=\"bg-light text-end x-small p-2\""
  container "$soc ($soc_family family), $sensor, $flash_size MB Flash. ${fw_version}-${fw_variant}. $hostname, $wan_mac"
_div

main_
  container_
    h2 "$page_title"
    flash_read
%>
