<% http_header_html %>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title><% html_title "$page_title" %></title>
<link rel="shortcut icon" href="/favicon.png">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
  integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
<link rel="stylesheet" href="/bootstrap.override.css">
<% if [ $HTTP_MODE = "development" ]; then %><link rel="stylesheet" href="/debug.css"><% fi %>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"
  integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
<script src="/main.js"></script>
</head>

<body id="top">
<nav class="navbar navbar-expand-lg navbar-dark sticky-top">
  <div class="container">
    <a class="navbar-brand" href="/cgi-bin/status.cgi"><img src="/img/logo.svg" width="116" height="32" alt=""></a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
      aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" id="dropdownInformation" href="#"
            role="button" data-bs-toggle="dropdown" aria-expanded="false">Information</a>
          <ul class="dropdown-menu" aria-labelledby="dropdownInformation">
            <li><a class="dropdown-item" href="/cgi-bin/status.cgi">Overview</a></li>
            <li><a class="dropdown-item" href="/cgi-bin/info/cron.cgi">Cron config</a></li>
            <li><a class="dropdown-item" href="/cgi-bin/info/dmesg.cgi">Diagnostic message</a></li>
            <li><a class="dropdown-item" href="/cgi-bin/info/httpd.cgi">HTTPd environment</a></li>
            <li><a class="dropdown-item" href="/cgi-bin/info/log.cgi">Log read</a></li>
          </ul>
        </li>
        <li class="nav-item"><a class="nav-link" href="/cgi-bin/firmware.cgi">Firmware</a></li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" id="dropdownNetwork" href="#"
            role="button" data-bs-toggle="dropdown" aria-expanded="false">Settings</a>
          <ul class="dropdown-menu" aria-labelledby="dropdownNetwork">
            <li><a class="dropdown-item" href="/cgi-bin/network.cgi">Network Settings</a></li>
            <li><a class="dropdown-item" href="/cgi-bin/network-ntp.cgi">NTP Settings</a></li>
            <li><a class="dropdown-item" href="/cgi-bin/webui-password.cgi">Web UI Password</a></li>
          </ul>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" id="dropdownMajestic" href="#"
            role="button" data-bs-toggle="dropdown" aria-expanded="false">Majestic</a>
          <ul class="dropdown-menu" aria-labelledby="dropdownMajestic">
            <li><a class="dropdown-item" href="/cgi-bin/majestic-settings-general.cgi">Settings</a></li>
            <li><a class="dropdown-item" href="/cgi-bin/majestic-settings-services.cgi">Services</a></li>
            <li><a class="dropdown-item" href="/cgi-bin/majestic-config-actions.cgi">Maintenance</a></li>
            <li><a class="dropdown-item" href="/cgi-bin/preview-help.cgi">Information</a></li>
          </ul>
        </li>
        <li class="nav-item  dropdown">
          <a class="nav-link dropdown-toggle" id="dropdownTools" href="#"
            role="button" data-bs-toggle="dropdown" aria-expanded="false">Tools</a>
          <ul class="dropdown-menu" aria-labelledby="dropdownTools">
            <li><a class="dropdown-item" href="/cgi-bin/tools.cgi">Ping & Traceroute</a></li>
            <li><a class="dropdown-item" href="/cgi-bin/console.cgi">Web Console</a></li>
          </ul>
        </li>
        <li class="nav-item"><a class="nav-link" href="/cgi-bin/preview.cgi">Preview</a></li>
      </ul>
    </div>
  </div>
</nav>
<main>
  <div class="container p-3">
